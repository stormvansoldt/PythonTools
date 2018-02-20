#!/usr/bin/python3

import json
from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

'''
Flow of the authentication and encryption process:
1. Public/private RSA keypair is generated on the client
2. Public key is sent to the server
3. Server determines a symmetric AES session key, which is then encrypted using
	the client's public RSA key
4. The client gets the encrypted response and deciphers it using the private
	RSA key.
5. Now that both parties have the session key, the encrypted communication can
	begin.  
'''

def generate_keypair():
	'''
	This function generates a public/private keypair, then writes them out
	to keys/pubkey.pem and keys/privkey.pem
	'''
	key_password 	= 'reallybadpassword'

	print('Generating RSA keypair...')
	key 		 	= RSA.generate(4096)

	pub_key			= key.publickey().exportKey()
	priv_key		= key.exportKey(passphrase=key_password,
									pkcs=8,
									protection='scryptAndAES128-CBC')

	with open('keys/privkey.pem', 'wb') as privfile:
		privfile.write(priv_key)

	with open('keys/pubkey.pem', 'wb') as pubfile:
		pubfile.write(pub_key)

	print('RSA keys successfully generated!')
	print('They have been stored in the keys/ directory.')

def session_keygen():
	'''
	Generate an AES-128 key to be used as the symmetric encryption key for the
	remainder of the communication. We then encrypt this key with the public 
	RSA key (which will be sent to us by the client), and return that encrypted
	session key.
	'''
	sesh_key = b'0123456789abcdef'		# CHANGE TO BE 16 RANDOM BYTES

	with open('keys/pubkey.pem', 'rb') as keyfile:
		pub_key = RSA.importKey(keyfile.read())

	rsa_cipher = PKCS1_OAEP.new(pub_key)

	return rsa_cipher.encrypt(sesh_key)

def decrypt_session_key(enc_key):
	'''
	Imports the private key, prompts for the passphrase, then uses the key
	to decrypt the content of the data argument. Returns the decrypted plain-
	text.

	THIS WILL BE RUN ON THE CLIENT.
	'''
	key_password = reallybadpassword

	with open('keys/privkey.pem', 'rb') as keyfile:
		priv_key = RSA.importKey(keyfile.read(), passphrase=key_password)

	rsa_cipher = PKCS1_OAEP.new(priv_key)

	return rsa_cipher.decrypt(data)


def encrypt_data(in_data):
	'''
	len(prefix) + in_bits/8 + len(suffix) = 16 (length of block size)
	'''
	prefix		= get_random_bytes(8)
	ctr 		= Counter.new(128)
	print(ctr)
	key 		= b'fedcba9876543210'
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	ciphertext	= aes_cipher.encrypt(in_data)

	print(ciphertext)

	return ciphertext, prefix

def decrypt_data(enc_in_data, prefix):
	'''
	Just decrypts shit.
	'''
	ctr 		= Counter.new(128)
	key 		= b'fedcba9876543210'
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	plaintext	= aes_cipher.decrypt(enc_in_data)

	print(plaintext)

ct, pf = encrypt_data(b'hello!')
decrypt_data(ct, pf)