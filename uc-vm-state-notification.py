#!/usr/bin/env python

import sys
import pika
import time
import random
import subprocess
import re

from pika.adapters import BlockingConnection

def create_channel():
    host = 'dev.rabbitmq.com'
    virtual_host = '/'
    user = 'guest'
    password = 'guest'

    credentials = pika.PlainCredentials(user, password)

    parameters = pika.ConnectionParameters(host=host,
                                           virtual_host=virtual_host,
                                           credentials=credentials)

    connection = BlockingConnection(parameters)
    channel = connection.channel()

    return (channel, parameters)


def get_expected_messages(vm_id):
    expected_messages = {}
    states = [ 'CREATE', 'RUNNING', 'DONE' ]
    for state in states:
        msg = 'VM_ID=%s; STATE=%s' % (vm_id, state)
        expected_messages[msg] = 1
    return expected_messages
     

def do_machine_lifecycle(parameters, queue):

    coords="dev.rabbitmq.com,/,guest,guest,%s" % (queue)
    print "Notification coordinates = %s" % (coords)
    cmd=["./uc-vm-state-notification.sh", coords]

    output=subprocess.check_output(cmd)
    print output

    regex = re.compile(".*VM ID=(\d+).*", re.DOTALL)
    matches = regex.findall(output)
    vm_id = matches[0]

    print "VM ID=%s" % (vm_id)

    return vm_id


def receive_messages(channel, queue, expected_messages):

    iterations = 0
    while (iterations < 10 and len(expected_messages) != 0):

        # Call basic get which returns the 3 frame types
        method_frame, header_frame, body = channel.basic_get(queue=queue)

        # Remove non-empty messages from the hash of expected ones.
        if method_frame.NAME != 'Basic.GetEmpty':
            print "Message body: %s" % (body)
            del(expected_messages[body])
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        # Increment the counter to stop if nothing is received.
        iterations += 1

        # No need to pound rabbit, sleep for a while.
        time.sleep(1)

    if len(expected_messages) != 0:
        error = 'unreceived message(s): '
        for message in expected_messages.keys():
            error += '"%s"\n' % message
        raise BaseException(error)

def create_random_queue(channel):
    queue = 'stratuslab-' + str(random.uniform(1000,9999))
    channel.queue_declare(queue=queue)
    #channel.queue_declare(queue=queue, durable=False,
    #                      exclusive=True, auto_delete=True)
    return queue


if __name__ == '__main__':

    (channel, parameters) = create_channel()

    queue = create_random_queue(channel)

    # Run a simple machine through its lifecycle.
    vm_id = do_machine_lifecycle(parameters, queue)

    # Expected messages from machine lifecycle.
    expected_messages = get_expected_messages(vm_id)

    # Receive messages; throws exception if not all are received.
    receive_messages(channel, queue, expected_messages)
