'''unpacker.py'''
import sys
from packer import marker
mlen = len(marker)

def unpack(ifile, prefix='new-'):
	for line in open(ifile):
		if line[:mlen] != marker:
			output.write(line)
		else:
			name = prefix + line[mlen:-1]
			print('creating:', name)
			output = open(name,'w')

if __name__ == '__main__':
	unpack(sys.argv[1])