#!/usr/bin/python3

import argparse
import socket

# TODO: Fix the rest of the argparse args, add nonblocking IO to server and client

def srv_init( host , port , sock ):
	'''
	This initializes the bind socket when 'nccopy -l' is used. The port param
	in the function declaration determines the port number that the script
	will listen on, and is passed in the command line.
	HOST is set to localhost (specifically '127.0.0.1') by default
	'''
	sock.bind((host , port))
	sock.listen(1)
	(conn , addr) = sock.accept()

	while True:
		try:
			msg = ((conn.recv(4096)).strip(b'\n')).decode('utf-8')
			print ('> ' + msg)
		except KeyboardInterrupt:
			print ('\nThanks for playing!')
			break

	sock.close()
	return 0

def client_init( host , port , sock ):
	'''
	Initializes the connection to the remote host on specified port number. 
	'''
	sock.connect((host , port))

	while True:
		try:
			msg = input() + '\n'
			sock.sendall(msg.encode(encoding='utf-8'))
		except KeyboardInterrupt:
			print('\nThanks for playing!')
			break

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

	msg		= ''
	args 	= parser.parse_args()
	sock 	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	print(args)

	if args.listen:
		srv_init(args.host, args.port, sock)
	else:
		client_init(args.host, args.port, sock)

if __name__ == '__main__':
	main()
