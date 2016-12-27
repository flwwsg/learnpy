'''bigpy-path.py'''
import sys, os, pprint
trace = 0 # 1 stands for direcory, 2 stands for file

visited = {}
allsizes = []
for srcdir in sys.path:
	for (thisDir, subsHere, filesHere) in os.walk(srcdir):
		if trace>0: print(thisDir)
		thisDir = os.path.normpath(thisDir)
		fixcase = os.path.normcase(thisDir)
		if fixcase in visited:
			continue
		for filename in filesHere:
			if filename.endswith('.py'):
				if trace>1: print('...', filename)
				pypath = os.path.join(thisDir, filename)
				try:
					pysize = os.path.getsize(pypath)
				except os.error:
					print('skipping', pypath, sys.exc_info()[0])
				else:
					pylines = len(open(pypath,'rb').readlines())
					allsizes.append((pysize, pylines, pypath))

print('By size ...')
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

print('By lines...')
allsizes.sort(key=lambda x: x[1])
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

