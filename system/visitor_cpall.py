#!/usr/bin/python3

import os
from visitor import FileVisitor
from cpall import copyfile

class CpallVisitor(FileVisitor):
	def __init__(self, fromDir, toDir, trace=True):
		self.fromDirLen = len(fromDir)
		self.toDir = toDir
		FileVisitor.__init__(self, trace=trace)

	def visitdir(self, dirpath):
		toPath = os.path.join(self.toDir, dirpath[self.fromDirLen:])
		if self.trace: print('d', dirpath, '=>', toPath)
		os.mkdir(toPath)
		self.dcount += 1

	def visitfile(self, fpath):
		toPath = os.path.join(self.toDir, fpath[self.fromDirLen:])
		if self.trace: print('f', fpath, '=>', toPath)
		copyfile(fpath, toPath)
		self.fcount += 1

if __name__ == '__main__':
	import sys, time
	fromDir, toDir = sys.argv[1:3]
	trace = len(sys.argv) > 3
	print('Copying...')
	start = time.clock()
	walker = CpallVisitor(fromDir, toDir, trace)
	walker.run(startdir=fromDir)
	print('Copied', walker.fcount, 'files', walker.dcount, 'directories', end=' ')
	print('in', time.clock() - start, 'seconds')
