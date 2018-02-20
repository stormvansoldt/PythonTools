#!/usr/bin/python3

import sys
from Crypto.Cipher import AES

def decrypt(key):
	'''
	Takes three arguments which are required to be passed to the decryption
	function in order to open the hardcoded file 'secret.bin'.
	'''
	with open('secret.bin', 'rb') as file:
		cipher_list = file.readlines()

	ciphertext	= cipher_list[0].strip(b'\n')
	nonce 		= cipher_list[1].strip(b'\n')
	tag			= cipher_list[2].strip(b'\n')

	cipher 		= AES.new(key, AES.MODE_EAX, nonce=nonce)
	plaintext 	= cipher.decrypt(ciphertext)
	print(plaintext)

decrypt(b'notagoodpassword')