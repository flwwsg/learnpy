'''getone.py'''
import os, sys
from getpass import getpass
from ftplib import FTP

nonpassive = False
filename = 'monkeys.jpg'
dirname = '.'
sitename = 'ftp.nosuch.site'
# userinfo = ('wdj',getpass('Password?'))
userinfo = ()
if len(sys.argv) > 1:
	filename = sys.argv[1]

print('Connecting...')
connection = FTP(sitename)
connection.login(*userinfo)
connection.cwd(dirname)
if nonpassive:
	connection.set_pasv(False)

print('Downloading...')
localfile = open(filename, 'wb')
connection.retrbinary('RETR '+filename, localfile.write)
connection.quit()
localfile.close()
