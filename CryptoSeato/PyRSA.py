#!/usr/bin/env python

import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

def generate_keypair():
	'''
	This function generates a new 2048-bit RSA keypair, and stores the public
	and private halves in pub_key and priv_key, respectively.

	Returns the keypair as a tuple.
	'''
	print('[*] Generating RSA keypair...')
	
	key 		 	= RSA.generate(2048)
	pub_key			= key.publickey().exportKey()
	priv_key		= key.exportKey(pkcs=8,
									protection='scryptAndAES128-CBC')

	print('[*] RSA keys successfully generated!')

	return (pub_key, priv_key)


def rsa_encrypt(msg, pub_key):
	'''
	Takes a msg (intended to be the raw 128-bit AES key, but can really be any
	data) as the first argument and encrypts it with the public RSA key passed
	as the second argument.

	Returns the encrypted message.
	'''
	pub_key 	= RSA.import_key(pub_key)
	rsa_cipher 	= PKCS1_OAEP.new(pub_key)

	return rsa_cipher.encrypt(msg)


def rsa_decrypt(enc_msg, priv_key):
	'''
	Takes an encrypted message and decrypts it using the private key passed
	as the second argument. 

	Returns the decrypted message.
	'''
	priv_key 	= RSA.import_key(priv_key)
	rsa_cipher 	= PKCS1_OAEP.new(priv_key)

	return rsa_cipher.decrypt(enc_msg)


#generate_keypair()
#aes_key = generate_sesh_key()
#print(decrypt_session_key(aes_key))