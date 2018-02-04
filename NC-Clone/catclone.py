#!/usr/bin/python3

import argparse
import socket
import sys
import threading
import time

'''
TODO: 	Fix the argparse options, add SIGINT/KeyboardInterrupt handling,
		clean up the ugly/redundant code.
'''

def send_msg( c ):
	while True:
		data = input() + '\n'
		if not data:
			break
		c.sendall(data.encode('utf-8'))

def recv_msg( c ):
	while True:
		data = ((c.recv(1024)).strip(b'\n')).decode('utf-8')
		if not data:
			break
		print(data)

def srv_init( addr ):
	'''
	If the program can successfully bind to a local host/port, return the
	connection object and close the original socket. Else, return 0
	'''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.bind(addr)
	except OSError:
		print('Error: this port is unavailable')
		return 1
	except PermissionError:
		print('Error: this port requires elevated permissions')
		return 1
	else:
		sock.listen(1)
		(conn , destination) = sock.accept()
		return conn
	finally:
		sock.close()

def client_init( addr ):
	'''
	If a successful connection is created, return the socket object containing
	the connection. Else, return 0
	'''
	try:
		return socket.create_connection(addr)
	except ConnectionRefusedError as e:
		print ('Error: unable to reach remote host')
		return 1

def main():
	'''
	The main function of our program. This uses the argparse library to get 
	args passed via the command line, associate them with flags, generate a
	usage output, and yell at the user if they don't provide sufficient and/or
	correct arguments.

	Then we get the socket object and create two new threads: one for receiving
	data, and one for catching STDIN and sending it to the remote client/server
	'''
	parser = argparse.ArgumentParser(
		   description='Simple copy of nc written in Python.')
	parser.add_argument('host',
						type=str,
						default='127.0.0.1',
						metavar='HOST',
						help='remote or local destination to connect/bind to')
	parser.add_argument('port',
						type=int,
						metavar='PORT',
						help='port to connect to/listen on')
	parser.add_argument('-l', 
						action='store_true',
						dest='listen',
						help='listen for a connection')

	args 	= parser.parse_args()
	addr 	= (args.host, args.port)

	if args.listen:
		conn = srv_init(addr)
	else:
		conn = client_init(addr)

	if conn == 1:
		sys.exit()

	t_recv 	= threading.Thread(target=recv_msg, args=[conn], daemon=True)
	t_send 	= threading.Thread(target=send_msg, args=[conn], daemon=True)
	t_recv.start()
	t_send.start()

	try:
		while True:
			time.sleep(0.5)
	except KeyboardInterrupt:
		sys.exit('Quitting program')
	finally:
		conn.close()

if __name__ == '__main__':
	main()
