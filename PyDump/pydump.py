#!/usr/bin/python3

import sys
import socket
import threading

# TODO: Implement the sexy_hex function

def sexy_hex(in_bytes):
	'''
	Take an input string (from either end of the data stream) and turn it 
	into a sexy output string showing the starting value, the hex value for
	each character, and the character string represented by the hex value.
	'''
	output_str	= ''
	LENGTH 		= 16
	in_str		= in_bytes.decode('UTF-8').strip('\n')
	chunks 		= [in_str[i:i+LENGTH] for i in range(0, len(in_str), LENGTH)]

	for index, chunk in enumerate(chunks):
		hex_str = ' '.join(['{:02X}'.format(ord(x)) for x in chunk])
		output_str += ('{0:#0{1}x}  {2:<50}{3}\n'.format(index, 4, hex_str, chunk))

	return(output_str)

def local_handler(l_sock, r_sock):
	'''
	Performs a recv() on the local socket, prints it, then pipes it to the
	remote socket.
	'''
	while True:
		data = l_sock.recv(1024)
		if not data:
			break
		print('[^] Recieved X bytes from localhost\n{}'.format(sexy_hex(data)))
		r_sock.sendall(data)
		print('[<--] Sent X bytes to remote host')

def remote_handler(l_sock, r_sock):
	'''
	Performs a recv() on the remote socket, prints the result, then pipes it 
	to the local socket.
	'''
	while True:
		data = r_sock.recv(1024)
		if not data:
			break
		print('[^] Recieved X bytes from remote\n{}'.format(sexy_hex(data)))
		l_sock.sendall(data)
		print('[-->] Sent X bytes to localhost')

def proxy_handler():
	'''
	Initialize the listening server so we can proxy our traffic through
	lhost:lport to rhost. This will allow us to print every byte of data
	sent and received through the connection to sniff for cool stuff.

	After the connections are established, create two new threads using
	remote_handler and local_handler to output from both ends of the pipe.

	Using the try:catch block waits for one/both of the threads using 
	thread.join(). If shit goes back, 
	'''
	rhost		= '127.0.0.1'
	lhost		= '127.0.0.1'
	rport		= 8001
	lport 		= 9001
	sock		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock.bind((lhost, lport))
	sock.listen(1)
	
	print('[*] Waiting for local connection...')
	(l_conn, l_addr) = sock.accept()

	print('[*] Received connection from {0!s}:{1!s}'.format(l_addr[0], l_addr[1]))
	
	print('[*] Connecting to rhost {0!s}:{1!s}...'.format(rhost, rport))
	r_conn		= socket.create_connection((rhost, rport))

	print('-----------------------------------------')
	print('| {0!s}:{1!s} =====> {2!s}:{3!s} |'.format(l_addr[0], l_addr[1], rhost, rport))
	print('| Connection established!               |')
	print('-----------------------------------------')

	t_remote	= threading.Thread(target=remote_handler, args=[l_conn, r_conn], daemon=True)
	t_local		= threading.Thread(target=local_handler, args=[l_conn, r_conn], daemon=True)
	t_remote.start()
	t_local.start()

	try:
		t_remote.join()
		t_local.join()
	except KeyboardException:
		print('SIGINT caught.')
	finally:
		print('Byebye!')
		l_conn.close()
		r_conn.close()
		sock.close()

def main():
	proxy_handler()

if __name__ == '__main__':
	main()