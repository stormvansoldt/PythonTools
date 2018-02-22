#!/usr/bin/env python

from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(plain_input, key):
	'''
	This function encrypts our incoming data using AES-128 CTR mode. First
	we generate a nonce made out of 8 random bytes that will serve as the 
	beginning of our counter function. Then we create a new Counter object
	by prefixing the nonce to another 8 null bytes (64 bits), which will
	increment for each block that gets encrypted.

	We then use this counter object and our secret key to create an AES
	cipher object which will then encrypt our payload. Finally we append the
	nonce to the beginning of that payload and return the completed cipher-
	text.
	'''
	ctr 		= Counter.new(64, get_random_bytes(8))
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	ciphertext	= aes_cipher.nonce + aes_cipher.encrypt(plain_input)

	return ciphertext

def decrypt(enc_input, key):
	'''
	This function simply does the reverse of our encrypt_data function and
	translates the incoming ciphertext into plaintext. The first 8 bytes of
	the enc_input are always going to be the nonce that we will use along-
	side the secret key to perform the decryption, so first we will store
	those bytes in the nonce variable.

	Then we use the nonce along with an additional 8 null bytes to create a
	Counter object, which is then piped into the AES.new function to create
	our decryption object. Then we pipe everything after the first 8 bytes of
	enc_input into the decrypt function of the AES object, and return the
	plaintext.
	'''
	nonce 		= enc_input[:8]
	ctr 		= Counter.new(64, nonce)
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	plaintext	= aes_cipher.decrypt(enc_input[8:])

	return plaintext