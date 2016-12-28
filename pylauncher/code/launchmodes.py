#!/usr/bin/python3
import os, sys

pyfile = (sys.platform[:3] == 'win' and 'python') or 'python3'
pypath = sys.executable 

def fixWindwsPath(cmdline):
	splitline = cmdline.lstrip().split(' ')
	fixedPATH = os.path.normpath(splitline[0])
	return ' '.join([fixedPATH] + splitline[1:])

class LaunchMode:
	def __init__(self, label, command):
		self.what = label
		self.where = command

	def __call__(self):
		self.announce(self.what)
		os.chdir(os.path.dirname(self.where))
		self.run(self.where)

	def announce(self, text):
		print(text)

	def run(self, cmdline):
		assert False, 'run must be defined!!!'

class System(LaunchMode):
	def run(self, cmdline):
		cmdline = fixWindwsPath(cmdline)
		os.system('"%s" %s' % (pypath, cmdline))

class Popen(LaunchMode):
	def run(self, cmdline):
		cmdline = fixWindwsPath(cmdline)		
		os.popen(pypath+' '+cmdline)

class Fork(LaunchMode):
	def run(self, cmdline):
		assert hasattr(os, 'fork')
		cmdline = cmdline.split()
		if os.fork() == 0:
			os.execvp(pypath, [pyfile] + cmdline)

class Start(LaunchMode):
	def run(self, cmdline):
		assert sys.platform[:3] == 'win'
		cmdline = fixWindwsPath(cmdline)
		os.startfile(cmdline)

class StartArgs(LaunchMode):
	def run(self, cmdline):
		assert sys.platform[:3] == 'win'
		os.system('start '+cmdline)

class Spawn(LaunchMode):
	def run(self, cmdline):
		os.spawnv(os.P_DETACH, pypath, (pyfile, cmdline))

class Top_level(LaunchMode):
	def run(self, cmdline):
		assert False, 'mod not yet implemented'

if sys.platform[:3] == 'win':
	PortableLauncher = Start
else:
	PortableLauncher = Fork

class QuietPortableLauncher(PortableLauncher):
	def announce(self, text):
		pass

def selftest():
	file = 'echo.py'
	input('default mode ...\n')
	launcher = PortableLauncher(file, file)
	launcher()

	input('System mode ...\n')
	System(file, file)()

	if sys.platform[:3] == 'win':
		input('DOS start mode...\n')
		StartArgs(file, file)()

if __name__ == '__main__':
	selftest()
