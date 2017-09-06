import os
import sys
import hashlib
import time
import cPickle as pickle

user=sys.argv[1]
global_dict={}
def printAbsPath(username):
    fullpath='/pxeusers/%s/%s'%(username,username)
    for root, dirs, files in os.walk(fullpath):
        for file in files:
            print(os.path.join(root, file))
            filepath=os.path.join(root, file)
            dedup(filepath,username)
            #print("")

def dedup(filepath,username):
    f = open(filepath, 'rb')
    data = f.read()
    f.close()
    bytes = len(data)
    inc = 4096
    fileNames = []
    for i in range(0, bytes+1, inc):
        hash_md5 = hashlib.md5()
        hash_md5.update(data[i:i+inc])
        fn1 = "file%s" % hash_md5.hexdigest()
        fileNames.append(fn1)
        f = open( os.path.join('/pxeusers/%s/hashedfile/'%username, fn1), 'wb')
        #f = open(fn1, 'wb')
        f.write(data[i:i+inc])
        f.close()
    global_dict[filepath]=fileNames
    pickle.dump( global_dict, open( "/pxeusers/%s/save.p"%username, "wb" ), protocol=2 )




print(time.asctime( time.localtime(time.time())))
printAbsPath(user)
print(time.asctime( time.localtime(time.time())))




