import os, os.path
import pika
import random
import time
import unittest

from pika.adapters import BlockingConnection

from usecases.TestUtils import *

class testVmStateNotification(unittest.TestCase):

    # minimal ttylinux image
    marketplaceId = 'PvitUfM-uW2yWakWUNmd-TSPOiy'

    vm_id = None
    vm_ip = None

    def create_channel(self):
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

    def get_expected_messages(self):
        expected_messages = {}
        states = [ 'CREATE', 'RUNNING', 'DONE' ]
        for state in states:
            msg = 'VM_ID=%s; STATE=%s' % (self.vm_id, state)
            expected_messages[msg] = 1
        return expected_messages

    def do_machine_lifecycle(self, parameters, queue):
        coords="dev.rabbitmq.com,/,guest,guest,%s" % (queue)
        print "Notification coordinates = %s" % (coords)

        self.vm_id, self.vm_ip = stratusRunInstance(self.marketplaceId, 
                                                    None, 
                                                    ['--notify', coords])
        waitVmRunningOrTimeout(self.vm_id)
        stratusKillInstance(self.vm_id)

    def receive_messages(self, channel, queue, expected_messages):

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


    def create_random_queue(self, channel):
        queue = 'stratuslab-' + str(random.uniform(1000,9999))
        channel.queue_declare(queue=queue)
        #channel.queue_declare(queue=queue, durable=False,
        #                      exclusive=True, auto_delete=True)
        return queue


    def setUp(self):
        return

    def tearDown(self):
        stratusKillInstance(self.vm_id)

    def test_usecase(self):

        (channel, parameters) = self.create_channel()

        queue = self.create_random_queue(channel)

        self.do_machine_lifecycle(parameters, queue)

        expected_messages = self.get_expected_messages()

        # Receive messages; throws exception if not all are received.
        self.receive_messages(channel, queue, expected_messages)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(testVmStateNotification)
