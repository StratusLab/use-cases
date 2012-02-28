
import os
import os.path
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib2

def readRemoteFile(url):
    fd = wget(url)
    return fd.read()

def wget(url):
    return urllib2.urlopen(url)
    
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

def stratusRunInstance(image, persistentDisk=None, options=None):
    cmd = ["stratus-run-instance", "--quiet", "--type", "m1.xlarge", image]
    if persistentDisk:
        cmd.extend(["--persistent-disk", persistentDisk ])
    if options:
        cmd.extend(options)
    response = execute(cmd)
    vm_id, vm_ip = response.split(', ')
    return (vm_id.strip(), vm_ip.strip())

def stratusDescribeInstance(vmId):
    return execute(["stratus-describe-instance", str(vmId)])

def stratusKillInstance(vmId):
    if vmId:
        execute(["stratus-kill-instance", str(vmId)])

def getVmState(vmId):
    lines = stratusDescribeInstance(vmId).split('\n')
    if len(lines) >= 2:
        return _extractState(lines[1])
    else:
        raise Exception('wrong number of lines (%d) from stratus-describe-instance' % len(lines))

def _extractState(line):
    trimmed = line.strip()
    fields = re.split('\s+', trimmed)
    return fields[1]

def waitVmRunningOrTimeout(vmId, timeout=(2*60), sleepInterval=5): 
    start = time.time()
    printStep('Started waiting for VM to be up at: %s' % start)
    state = ''
    while state != 'Running' and ((time.time() - start) < timeout):
        state = getVmState(vmId)
        print "\tStatus of VM '%s' is  '%s'" % (vmId, state)
        if state == 'Failed':
            raise Exception('VM (%s) failed to start' % vmId)
        time.sleep(sleepInterval)

    if state != 'Running':
        raise Exception('VM (%s) timed out' % vmId)

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

def createDummyImage(digits=1024):
    file_descriptor, filename = tempfile.mkstemp()

    file = None
    try:
        file = open(filename, 'w')
        for i in range(0, digits):
            file.write(randomDigit())
    except Exception as e:
        print e
        raise e
    finally:
        closeFileReliably(file)

    return (file_descriptor, filename)

def randomDigit():
    return str(random.choice(xrange(0,10)))

def removeFile(file):
    if (file):
        try:
            os.remove(file)
        except Exception as e:
            print e

def closeFileReliably(file):
    if (file):
        try:
            file.close()
        except Exception as e:
            print e

def closeFileDescriptorReliably(file_descriptor):
    if (file_descriptor):
        try:
            os.close(file_descriptor)
        except Exception as e:
            print e

def stratusBuildMetadata(image):
    execute(["stratus-build-metadata",
             "--author=Alice Smith",
             "--os=dummyos", 
             "--os-version=0.0", 
             "--os-arch=i686",
             "--image-version=1.0", 
             image])

def expectedMetadataFilename():
    return "%s-%s-%s-base-%s.xml" % ("dummyos", "0.0", "i686", "1.0")

def stratusSignMetadata(image):
    execute(["stratus-sign-metadata", image]) 

def stratusValidateMetadata(metadata):
    execute(["stratus-validate-metadata", "-vvv", metadata])

def stratusUploadMetadata(metadata):
    return execute(["stratus-upload-metadata", "-vvv", metadata])

def stratusDeprecateMetadata(identifier, email, reason="Just For Fun"):
    return execute(["stratus-deprecate-metadata", 
                    "--email", email,
                    "--reason", reason,
                    identifier
                    ])

def ssh(ip='localhost', cmd='/bin/true', user='root'):
    ssh_id = "%s@%s" % (user, ip)
    ssh_cmd = ['ssh', ssh_id, '-q', 
               '-o', 'ConnectTimeout=5', 
               '-o', 'StrictHostKeyChecking=false', 
               cmd]
    execute(ssh_cmd)

def sshConnectionOrTimeout(ip='localhost', user='root', timeout=(2*60), sleepInterval=5):
    start = time.time()
    printStep('Started trying to SSH to VM: %s' % start)
    while ((time.time() - start) < timeout):
        try:
            ssh(ip, '/bin/true', user)
            return
        except Exception:
            time.sleep(sleepInterval)
    raise Exception('timeout exceeded while trying SSH')
