'''testargv2.py'''
def getops(argv):
	opts = {}
	print(argv)
	while argv:
		if argv[0][0] == '-':
			opts[argv[0]] = argv[1]
			argv = argv[2:]	
		else:
			argv = argv[1:]
	return opts

if __name__ == '__main__':
	from sys import argv
	myargs = getops(argv)
	if '-i' in myargs:
		print(myargs['-i'])
	print(myargs)