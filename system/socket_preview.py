'''socket_preview.py'''

from socket import socket, AF_INET, SOCK_STREAM

port = 50008
host = 'localhost'

def server():
	sock = socket(AF_INET, SOCK_STREAM)
	# hname = socket.gethostname()
	sock.bind(('', port))
	sock.listen(5)
	while True:
		conn, addr = sock.accept()
		data = conn.recv(1024)
		text = data.decode()
		if text=='quit':
			print('quit now')
			exit()
		reply = 'server got: [%s]' % data
		conn.send(reply.encode())

def client(name):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((host, port))
	sock.send(name.encode())
	reply = sock.recv(1024)
	sock.close()
	print('client got:[%s]' % reply)

if __name__ == '__main__':
	from threading import Thread
	sthread = Thread(target = server)
	sthread.daemon = True
	sthread.start()
	for i in range(5):
		Thread(target=client, args=('client%s' % i,)).start()
	# client('quit')