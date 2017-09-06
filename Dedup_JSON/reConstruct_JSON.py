import hashlib
import os
import sys
import json
import time

#global_dict = pickle.load( open( "/home/cs/save.p", "rb" ) )
with open('/pxeusers/%s/save.json' %username, 'r') as fp:
	global_dict=json.load(fp)
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