#!/usr/bin/env python

import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

def generate_keypair():
	'''
	This function takes a user-defined input as a password, then uses it to
	generate a 4096-bit public and private RSA keypair. These keys are then 
	saved to ~/.pykeys/ in the user's home directory as "private.key" and
	"public.key".

	Returns a tuple containing the keypair in the form (pub_key, priv_key)
	'''
	path			= os.path.expanduser('~/') + '.pykeys/'

	if os.path.isfile(path + 'private.key'):
		print('[!] WARNING: it looks like a private and/or public key already exists. If you continue, those keys will be overwritten!')
		print('[!] Are you sure you want to continue? (y/n)')
		answer = input().lower()

		if answer == 'n':
			print('[*] Don\'t worry, your keys are safe!')
			return 0
		elif answer == 'y':
			print('[*] Overwriting old key files...')
		else:
			print('[!] Unknown input. Shutting down, notifying Skynet')
			return 1

	print('[*] Generating RSA keypair...')
	
	key 		 	= RSA.generate(2048)
	pub_key			= key.publickey().exportKey()
	priv_key		= key.exportKey(pkcs=8,
									protection='scryptAndAES128-CBC')

	if not os.path.isdir(path):
		print('[*] Creating \'~/.pykeys/\' directory...')
		os.makedirs(path)

	with open(path + 'private.key', 'wb') as privfile:
		print('[*] Exporting private key...')
		privfile.write(priv_key)

	with open(path + 'public.key', 'wb') as pubfile:
		print('[*] Exporting public key...')
		pubfile.write(pub_key)

	print('[*] RSA keys successfully generated!')
	print('[*] They have been stored in {}'.format(path))

	return (pub_key, priv_key)


def rsa_encrypt(key):
	'''
	Generate an AES-128 key to be used as the symmetric encryption key for the
	remainder of the communication. We then encrypt this key with the public 
	RSA key (which will be sent to us by the client), and return that encrypted
	session key.
	'''
	path		= os.path.expanduser('~/') + '.pykeys/'

	with open(path + 'public.key', 'rb') as keyfile:
		pub_key = RSA.importKey(keyfile.read())

	rsa_cipher 	= PKCS1_OAEP.new(pub_key)

	return rsa_cipher.encrypt(key)


def rsa_decrypt(enc_key):
	'''
	Imports the private key, prompts for the passphrase, then uses the key
	to decrypt the content of the data argument. Returns the decrypted plain-
	text.

	THIS WILL BE RUN ON THE CLIENT.
	'''
	path			= os.path.expanduser('~/') + '.pykeys/'

	with open(path + 'private.key', 'rb') as keyfile:
		priv_key = RSA.importKey(keyfile.read())

	rsa_cipher = PKCS1_OAEP.new(priv_key)

	return rsa_cipher.decrypt(enc_key)


#generate_keypair()
#aes_key = generate_sesh_key()
#print(decrypt_session_key(aes_key))