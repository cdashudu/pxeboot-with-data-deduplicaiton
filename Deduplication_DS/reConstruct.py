import hashlib
import os
import sys
import cPickle as pickle
import time
username=sys.argv[1]
#global_dict = pickle.load( open( "/pxeusers/username/save.p", "rb" ) )
global_dict = pickle.load( open( '/pxeusers/%s/save.p' %username, "rb" ) )

#Start Time
print(time.asctime( time.localtime(time.time())))

for key,value in global_dict.iteritems():
	print ("Generating file %s" % key)
	filename=key
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc:# Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	dataList = []
	fileNames = global_dict[key]
	for fn in fileNames:
		f = open(os.path.join('/pxeusers/%s/hashedfile/'%username, fn), 'rb')
		dataList.append(f.read())
		f.close()

	f = open(filename, 'wb')
	for data in dataList:
		f.write(data)
	f.close
#End Time
print(time.asctime( time.localtime(time.time())))