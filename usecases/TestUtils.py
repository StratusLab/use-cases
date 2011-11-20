
import os
import os.path

def which(file):
    for path in os.environ["PATH"].split(os.pathsep):
        if file in os.listdir(path):
            print "%s/%s" % (path, file)


