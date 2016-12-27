#!/usr/bin/env python3
import ftplib
from os.path import basename
def putfile(file, site, dir, user=(), *, verbose=True):
	if verbose: print('Uploading', file)
	local = open(file, 'rb')
	remote = ftplib.FTP(site)
	remote.login(*user)
	remote.cwd(dir)
	remote.storbinary('STOR '+file, local)
	remote.quit()
	local.quit()
	if verbose: print('Upload done')

if __name__ == '__main__':
	site = '117.78.44.138'
	dir = '.'
	import sys, getpass
	pswd = getpass.getpass(site + ' pswd?')
	putfile(sys.argv[1], site, dir, user=('wdj', pswd))