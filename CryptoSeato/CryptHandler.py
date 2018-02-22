#!/usr/bin/env python

import sys
import socket
import PyAES
import PyRSA
from Crypto.Random import get_random_bytes

'''
This module has functions that will perform the necessary handling of 
the private key exchange and generation of passphrases.

1. Client connects to server
2. Client generates RSA keypair
3. Client sends pubkey to server
4. Server accepts pubkey
5. Server generates session key
6. Server encrypts session key
7. Server sends encrypted session key to the client
8. Client accepts session key
9. Client decrypts session key
10. Main loop begins
'''

def server_handler(l_host, l_port):
	sock 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((l_host, l_port))

	print('[ ] Waiting for remote connection...')
	sock.listen(1)
	
	conn, addr	= sock.accept()
	print('[*] Received connection from {0}:{1}'.format(addr[0], addr[1]))

	print('[ ] Waiting to receive client\'s public key...')
	pub_key 	= conn.recv(2048)
	print('[*] Received public key!')

	print('[ ] Generating AES session key and encrypting it with the public RSA key...')
	session_key	= get_random_bytes(16)

	print('[*] Sending AES key to client')
	conn.sendall(PyRSA.rsa_encrypt(session_key, pub_key))

	print(session_key)
	print('Adios!')
	conn.close()
	sock.close()

	return session_key


def client_handler(r_host, r_port):
	print('Attempting to connect to remote host...')
	conn 	= socket.create_connection((r_host, r_port))
	print('Connected to server!')

	print('Begin RSA key generation...')
	(pub_key, priv_key) = PyRSA.generate_keypair()

	print('Sending RSA public key to server')
	conn.sendall(pub_key)

	print('Waiting to receive the encrypted session key...')
	enc_session_key 	= conn.recv(4096)

	print('Received encrypted session key!')
	session_key 		= PyRSA.rsa_decrypt(enc_session_key, priv_key)

	print('Decrypted the session key!')
	print(session_key)
	print('Goodbye!')
	conn.close()

	return session_key

def main():
	arg = sys.argv[1]

	if arg == 'l':
		server_handler('0.0.0.0', 32123)
	elif arg == 'c':
		client_handler('127.0.0.1', 32123)
	else:
		print('try again asshole')

if __name__ == '__main__':
	main()