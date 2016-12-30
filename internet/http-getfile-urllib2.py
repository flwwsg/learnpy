#!/usr/bin/python3
import sys, os, urllib.request, urllib.parse
showlines = 6

try:
	servername, filename = sys.argv[1:3]
except:
	servername, filename = 'baidu.com', '/index.html'

remoteaddr = 'http://%s%s' % (servername, filename)
if len(sys.argv) == 4:
	localname = sys.argv[3]
else:
	(scheme, server, path, parms, query, frag) = urllib.parse.urlparse(remoteaddr)
	localname = os.path.split(path)[1]

print(remoteaddr, localname)
urllib.request.urlretrieve(remoteaddr, localname)
remotdata = open(localname, 'rb').readlines()
for line in remotdata[:showlines]:
	print(line)