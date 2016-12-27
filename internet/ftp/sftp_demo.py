#!/usr/bin/python3
import pysftp
from getpass import getpass

host = '117.78.44.138'
username = 'wdj'
pwd = getpass('password for %s on %s?' % (username, host))
with pysftp.Connection(host, username=username, password=pwd) as sftp:
    with sftp.cd('py3'):             # temporarily chdir to public
        # sftp.put('/my/local/filename')  # upload file to public/ on remote
        sftp.get('wiki8.py') 