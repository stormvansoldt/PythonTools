#!/usr/bin/python3

import argparse
import socket
import sys
import threading

# TODO: Fix the rest of the argparse args, add nonblocking IO to the client

def send_msg(c):
	while True:
		data = input() + '\n'
		if not data:
			break
		c.sendall(data.encode('utf-8'))

def recv_msg(c):
	while True:
		msg = ((c.recv(1024)).strip(b'\n')).decode('utf-8')
		if not msg:
			break
		print(msg)

def srv_init( host , port , sock ):
	'''
	This initializes the bind socket when 'nccopy -l' is used. The port param
	in the function declaration determines the port number that the script
	will listen on, and is passed in the command line.
	HOST is set to localhost (specifically '127.0.0.1') by default
	'''
	try:
		sock.bind((host , port))
		sock.listen(1)
		(conn , addr) = sock.accept()
	except OSError as e:
		print ('Error: this port is unavailable')
		return 0

	t_recv = threading.Thread(target=recv_msg, args=[conn])
	t_send = threading.Thread(target=send_msg, args=[conn])
	t_recv.start()
	t_send.start()

	sock.close()
	return 0


def client_init( host , port , sock ):
	'''
	Initializes the connection to the remote host on specified port number. 
	'''
	try:
		conn = socket.create_connection((host , port))
	except ConnectionRefusedError as e:
		print ('Error: unable to reach remote host')
		return 0

	t_recv = threading.Thread(target=recv_msg, args=[conn])
	t_send = threading.Thread(target=send_msg, args=[conn])
	t_recv.start()
	t_send.start()

	sock.close()
	return 0

def main():
	'''
	The main function of our program. This uses the argparse library to get 
	args passed via the command line, associate them with flags, generate a
	usage output, and yell at the user if they don't provide sufficient and/or
	correct arguments.
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
	sock 	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# This is a debugging message - delete when finished
	print(args)

	if args.listen:
		srv_init(args.host, args.port, sock)
	else:
		client_init(args.host, args.port, sock)

if __name__ == '__main__':
	main()
