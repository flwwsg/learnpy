'''getfile-ftp.py'''
from ftplib import FTP
from os.path import exists, basename

def getfile(file, site, dir, user=(), *, verbose=True, refetch=False):
	if exists(file) and not refetch:
		if verbose: print(file, 'already fetched')
	else:
		if verbose: print('Downloading', file)
		local = open(basename(file), 'wb')
		try:
			remote = FTP(site)
			remote.login(*user)
			remote.cwd(dir)
			remote.retrbinary('RETR '+file, local.write)
			remote.quit()
		finally:
			local.close()
		if verbose: print('Download done.')

if __name__=='__main__':
	file = 'robots.txt'
	# file = 'WIAB1E.zip'
	dir = '.'
	site = 'ftp.sjtu.edu.cn'

	# import getpass
	# pwd = getpass.getpass(site+' password?')
	# user = ('wdj', pwd)
	user = tuple()
	getfile(file, site, dir, user=user)