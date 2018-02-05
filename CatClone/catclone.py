#!/usr/bin/python3

import argparse
import socket
import sys
import threading

'''
TODO: 	Refactor ugly and redundant code
'''

def send_msg( c ):
	while True:
		data = input() + '\n'
		c.sendall(data.encode('utf-8'))

def recv_msg( c ):
	while True:
		data = (c.recv(1024)).decode('utf-8')
		if not data:
			print('[*] Connection closed by remote host')
			break
		print(data.strip('\n'))

def srv_init( addr ):
	'''
	If the program can successfully bind to a local host/port, return the
	connection object and close the original socket. Else, return 1
	'''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.bind(addr)
	except OSError:
		print('[!] Error: this port is unavailable')
		return 1
	except PermissionError:
		print('[!] Error: this port requires elevated permissions')
		return 1
	else:
		sock.listen(1)
		print('[*] Listening on {0!s}:{1!s}...'.format(addr[0], addr[1]))
		(conn , dest) = sock.accept()
		print('[*] Received connection from {0!s} on port {1!s}!'.format(dest[0], dest[1]))
		return conn
	finally:
		sock.close()

def client_init( addr ):
	'''
	If a successful connection is created, return the socket object containing
	the connection. Else, return 1
	'''
	try:
		conn = socket.create_connection(addr)
	except ConnectionRefusedError:
		print ('[!] Error: unable to reach remote host')
		return 1
	else:
		print('[*] Connected to {0!s}!'.format(addr[0]))
		return conn

def main():
	'''
	The main function of our program. This uses the argparse library to get 
	args passed via the command line, associate them with flags, generate a
	usage output, and yell at the user if they don't provide sufficient and/or
	correct arguments.

	Then we get the socket object and create two new threads: one for receiving
	data, and one for catching STDIN and sending it to the remote client/server.
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
		t_recv.join()
	except KeyboardInterrupt:
		sys.exit('\n[*] Thanks for using CatClone!')
	finally:
		conn.close()

if __name__ == '__main__':
	main()
