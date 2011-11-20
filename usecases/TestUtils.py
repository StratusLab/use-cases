
import os
import os.path
import subprocess
import sys
import time

def which(file):
    for path in os.environ["PATH"].split(os.pathsep):
        if file in os.listdir(path):
            return os.path.join(path, file)

def stratuslabBinDir():
    location = which('stratus-describe-instance')
    return os.path.dirname(location)

def execute(cmd, returnType=None, exit=True, quiet=False, shell=False):
    printCmd(' '.join(cmd))
    if quiet:
        devNull = open(os.devnull, 'w')
        stdout = devNull
        stderr = devNull
    else:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, shell=shell)
    p.wait()
    if quiet:
        devNull.close()
    if returnType:
        return p.returncode
    else:
        out = p.stdout.read()
        err = p.stderr.read()
        if p.returncode == 0:
            if not quiet:
                if out:
                    printAndFlush(out + '\n')
                if err:
                    printAndFlush(err + '\n')
            return out
        else:
            printAndFlush('  [ERROR] Error executing command!\n')
            if out:
                printAndFlush(out + '\n')
            if err:
                printAndFlush(err + '\n')
            if exit:
                raise Exception

def printAndFlush(msg):
    sys.stdout.flush()
    print msg,
    sys.stdout.flush()

def printAction(msg):
    printAndFlush('\n :::%s:::\n' % (':' *len(msg)))
    printAndFlush(' :: %s ::\n' % msg)
    printAndFlush(' :::%s:::\n' % (':' *len(msg)))

def printStep(msg):
    printAndFlush(' :: %s\n' % msg)

def printCmd(msg):
    printAndFlush('  [Executing] %s\n' % msg)

def stratusRunInstance(image, persistentDisk=None):
    cmd = ["stratus-run-instance", "--quiet", image]
    if persistentDisk:
        cmd.extend(["--persistent-disk", persistentDisk ])
    response = execute(cmd)
    return response.split(', ')

def stratusDescribeInstance(vmId):
    return execute(["stratus-describe-instance", str(vmId)])

def stratusKillInstance(vmId):
    if vmId:
        execute(["stratus-kill-instance", str(vmId)])

def getVmState(vmId):
    return stratusDescribeInstance(vmId).split('\n')[1].split(' ')[1]

def waitVmRunningOrTimeout(vmId, timeout=(5*60), sleepInterval=5): 
    start = time.time()
    printStep('Started waiting for VM to be up at: %s' % start)
    state = ''
    while state != 'Running' and ((time.time() - start) < timeout):
        state = getVmState(vmId)
        print "\tStatus of VM '%s' is  '%s'" % (vmId, state)
        if state == 'Failed':
            break
        time.sleep(sleepInterval)
    return state

def stratusCreateVolume(size=1, tag='test-disk'):
    response = execute(["stratus-create-volume", "--size=%s" % size, "--tag=%s" % tag])
    return response.split(" ")[1].replace('\n', '')

def stratusDeleteVolume(uuid):
    if (uuid):
        execute(["stratus-delete-volume", uuid])

def stratusDescribeVolumes(uuid=None):
    cmd = ["stratus-describe-volumes"]
    if uuid:
        cmd.append(uuid)
    return execute(cmd)

def stratusAttachVolume(vmId, uuid):
    return execute(["stratus-attach-volume", "-i", str(vmId), uuid])

def stratusDetachVolume(vmId, uuid):
    return execute(["stratus-detach-volume", "-i", str(vmId), uuid])
