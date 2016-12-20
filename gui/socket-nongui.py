'''socket-nongui.py'''
import time, sys
if len(sys.argv) > 1:
	from socket_stream_redirect0 import *
	redirectOut()

while True:
	print(time.asctime())
	sys.stdout.flush()
	time.sleep(2.0)

