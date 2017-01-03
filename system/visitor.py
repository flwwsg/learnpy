import os, sys
class FileVisitor(object):
	def __init__(self, context=None, trace=2):
		self.fcount = 0
		self.dcount = 0
		self.context = context
		self.trace = trace

	def run(self, startdir=os.curdir, reset=True):
		if reset: self.reset()
		for (thisDir, dirsHere, filesHere) in os.walk(startdir):
			self.visitdir(thisDir)
			for fname in filesHere:
				fpath = os.path.join(thisDir, fname)
				self.visitfile(fpath)

	def reset(self):
		self.fcount = self.dcount = 0

	def visitdir(self, dirpath):
		self.dcount += 1
		if self.trace > 0: print(dirpath, '...')

	def visitfile(self, filepath):
		self.fcount += 1
		if self.trace > 1: print(self.fcount, '=>', filepath)

class SearchVisitor(FileVisitor):
	skipexts = ['.gif', '.jpg', '.pyc', '.exe']
	textexts = ['.txt', '.py', '.pyw', '.html','.c','.h']
	def __init__(self, searchkey, trace=2):
		FileVisitor.__init__(self, searchkey, trace)
		self.scount = 0

	def reset(self):
		self.scount = 0

	def candidate(self, fname):
		ext = os.path.splitext(fname)[1]
		if self.textexts:
			return ext in self.textexts
		else:
			return ext not in self.skipexts

	def visitfile(self, fname):
		FileVisitor.visitfile(self,fname)
		if not self.candidate(fname):
			if self.trace > 0: print('Skipping', fname)
		else:
			text = open(fname).read()
			if self.context in text:
				self.visitmatch(fname, text)
				self.scount += 1
	def visitmatch(self, fname, text):
		print('%s has %s' % (fname, self.context))

if __name__ == '__main__':
	dolist = 1
	dosearch = 2
	donext = 4

	def selftest(testmask):
		if testmask & dolist:
			visitor = FileVisitor(trace=2)
			visitor.run(sys.argv[2])
			print('Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount))

		if testmask & dosearch:
			visitor = SearchVisitor(sys.argv[3], trace=0)
			visitor.run(sys.argv[2])
			print('Found in %d files, visited %d' % (visitor.scount, visitor.fcount))

	selftest(int(sys.argv[1]))