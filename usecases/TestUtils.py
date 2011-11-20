
import os
import os.path
import subprocess
import sys

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
        devNull = open('/dev/null', 'w')
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




