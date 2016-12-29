#!/usr/bin/python3 
import os, sys, glob, time
from subprocess import Popen, PIPE

testdir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
forcegen = len(sys.argv) > 2
print('Start tester:', time.asctime())
print('in', os.path.abspath(testdir))

def verbose(*args):
	print('-'*80)
	for arg in args: print(arg)

def quiet(*args):
	pass

testpatt = os.path.join(testdir, 'Scripts', '*.py')
testfiles = glob.glob(testdir)
testfiles.sort()
trace(os.getcwd(), *testfiles)

numfail = 0 
for testpath in testfiles:
	testname = os.path.basename(testpath)
	infile = testname.replace('.py', '.in')
	inpath = os.path.join(testdir, 'Inputs', infile)
	indata = open(inpath, 'rb').read() if os.path.exists(inpath) else b''

	argfile = testname.replace('.py', '.args')
	argpath = os.path.join(testdir, 'Args', argfile)
	argdata = open(argpath).read() if os.path.exists(argpath) else ''

	outfile = testname.replace('.py', '.out')
	outpath = os.path.join(testdir, 'Outputs', outfile)
	outpathbad = outpath + '.bad'
	if os.path.exists(outpathbad): os.remove(outpathbad)

	errfile = testname.replace('.py', '.err')
	errpath = os.path.join(testdir, 'Errors', errfile)
	if os.path.exists(errpath): os.remove(errpath)

	pypath = sys.executable
	command = '%s %s %s' % (pypath, testpath, argdata)
	trace(command, indata)

	process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	process.stdin.write(indata)
	process.stdin.close()
	outdata = process.stdout.read()
	errdata = process.stderr.read()
	exitstatus = process.wait()
	trace(outdata, errdata, exitstatus)

	if exitstatus != 0:
		print('ERROR status:', testname, exitstatus)

	if errdata:
		print('ERROR stream:', testname, errpath)
		open(errpath, 'wb').write(outdata)

	if exitstatus or errdata:
		numfail += 1
		open(outpathbad, 'wb').write(outdata)
	elif not os.path.exists(outpath) or forcegen:
		print('generating:', outpath)
		open(outpath, 'wb').write(outdata)
	else:
		priorout = open(output, 'rb').read()
		if priorout == outdata:
			print('passed:', testname)
		else:
			numfail += 1
			print('FAILED output:', testname, outpathbad)
			open(outpathbad, 'wb').write(outdata)

print('Finished:', time.asctime())
print('%s tests were run, %s tests failed.' % (len(testfiles, numfail)))