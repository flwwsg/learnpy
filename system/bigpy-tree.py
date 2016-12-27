'''bigpy-tree.py'''
import sys, os, pprint
trace = False
if sys.platform.startswith('win'):
	exit('Not implemented!')
else:
	dirname = '/usr/lib64/python3.4'
allsize = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
	if trace: print(thisDir)
	for filename in filesHere:
		if filename.endswith('.py'):
			if trace: print('...', filename)
			fullname = os.path.join(thisDir, filename)
			fullsize = os.path.getsize(fullname)
			allsize.append((fullsize, fullname))
allsize.sort()
pprint.pprint(allsize[:2])
pprint.pprint(allsize[-2:])