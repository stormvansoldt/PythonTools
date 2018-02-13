#!/usr/bin/python3

import sys
import socket
import threading
import argparse

# TODO: Possibly refactor remote_handler and local_handler into one function
#		Add on-the-fly data manipulation

def sexy_hex(in_bytes):
	'''
	Take an input bytes object (from either end of the data stream) and turn it 
	into a sexy output string showing the starting value, the hex value for
	each character, and the character string represented by the hex value.

	Returns a tuple where the first element is the entire sexified hex output,
	and the second element is the length of the input string.
	'''
	output_str	= ''
	LENGTH 		= 16
	in_str		= in_bytes.decode('UTF-8').strip('\n')
	output_len	= len(in_str)
	chunks 		= [in_str[i:i+LENGTH] for i in range(0, len(in_str), LENGTH)]

	for index, chunk in enumerate(chunks):
		hex_str 	= ' '.join(['{:02X}'.format(ord(x)) for x in chunk])
		output_str += ('{0:#0{1}x}  {2:<50}{3}\n'.format(index, 4, hex_str, chunk))

	output_str 	= output_str.rstrip('\n')
	return((output_str, output_len))

def local_handler(l_sock, r_sock):
	'''
	Performs a recv() on the local socket. Sexifies that data and prints it,
	then sends the raw data out to the remote host.
	'''
	while True:
		data = l_sock.recv(1024)
		if not data:
			break
		sexy_out, data_len = sexy_hex(data)
		print('[ ^ ] Recieved {0} bytes from localhost\n{1}'.format(data_len, sexy_out))
		r_sock.sendall(data)
		print('[<--] Sent {} bytes to remote host\n'.format(data_len))

def remote_handler(l_sock, r_sock):
	'''
	Performs a recv() on the remote socket. Sexifies that data and prints it,
	then sends the raw data back to the local client.
	'''
	while True:
		data = r_sock.recv(1024)
		if not data:
			break
		sexy_out, data_len = sexy_hex(data)
		print('[ ^ ] Recieved {0} bytes from remote\n{1}'.format(data_len, sexy_out))
		l_sock.sendall(data)
		print('[-->] Sent {} bytes to localhost\n'.format(data_len))

def proxy_handler():
	'''
	Initialize the listening server so we can proxy our traffic through
	lhost:lport to rhost. This will allow us to print every byte of data
	sent and received through the connection to sniff for cool stuff.

	After the connections are established, create two new threads using
	remote_handler and local_handler to output from both ends of the pipe.

	Using the try:catch block waits for one/both of the threads using 
	thread.join(). Since the threads are daemonized, we ensure both are
	killed when the program closes.
	'''

	parser = argparse.ArgumentParser(
		   description='TCP proxy written in Python because Python is awesome.')
	parser.add_argument('l_port',
						type=int,
						metavar='PORT',
						help='local port to bind the listener to')
	parser.add_argument('target',
						type=str,
						metavar='TARGET',
						help='remote host to connect to in the form of (IP:PORT)')

	args 			= parser.parse_args()
	r_host, r_port	= tuple(args.target.split(':'))
	proxy_addr		= ('127.0.0.1', args.l_port)
	sock			= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.bind(proxy_addr)
	sock.listen(1)
	
	print('[*] Waiting for local connection...')
	(l_conn, l_addr) = sock.accept()

	print('[*] Received connection from {0!s}:{1!s}'.format(l_addr[0], l_addr[1]))
	
	print('[*] Connecting to {0!s}:{1!s}...'.format(r_host, r_port))
	r_conn		= socket.create_connection((r_host, r_port))

	print('-----------------------------------------')
	print('| {0!s}:{1!s} =====> {2!s}:{3!s} |'.format(l_addr[0], l_addr[1], r_host, r_port))
	print('| Connection established!               |')
	print('-----------------------------------------\n')

	t_remote	= threading.Thread(target=remote_handler, args=[l_conn, r_conn], daemon=True)
	t_local		= threading.Thread(target=local_handler, args=[l_conn, r_conn], daemon=True)
	t_remote.start()
	t_local.start()

	try:
		t_remote.join()
		t_local.join()
	except KeyboardException:
		print('[!] SIGINT caught')
	finally:
		print('[*] Closing socket connections')
		l_conn.close()
		r_conn.close()
		sock.close()

def main():
	proxy_handler()

if __name__ == '__main__':
	main()