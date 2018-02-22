#!/usr/bin/env python

from Crypto.Util import Counter
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(plain_input, key):
	'''
	Generate counter object to utilize with AES-CTR mode, where the initial
	value is 8 randomly generated bytes prefixed to 8 null bytes. Use this
	counter and the secret key passed as an argument to create an AES cipher
	object. Then encrypt the plain_input argument and prefix the randomly
	generated bytes as a nonce, and store the message in ciphertext variable.

	Keyword arguments:
	 plain_input -- the message to be encrypted by the function
	 key 		 -- passphrase used to encrypt the message. must be 16 bytes
	 				long.

	Returns:
	 ciphertext	 -- the 8 byte nonce + the encrypted message
	'''
	ctr 		= Counter.new(64, get_random_bytes(8))
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	ciphertext	= aes_cipher.nonce + aes_cipher.encrypt(plain_input)

	return ciphertext

def decrypt(enc_input, key):
	'''
	Take the first 8 bytes from the encoded input and save it as the nonce.
	Create a new counter object using the nonce prefixed to 8 null bytes, and
	use that counter and the secret key to create a new AES cipher object. 
	Pass the remainer of the encoded input (after the first 8 bytes) to the
	cipher object to perform the decryption, and store the result in the
	plaintext variable.

	Keyword arguments:
	 enc_input	-- the encrypted ciphertext prefixed with the nonce
	 key 		-- passphrased used to decrypt the message. must be 16 bytes
					long.

	Returns:
	 plaintext 	-- the decrypted ciphertext
	'''
	nonce 		= enc_input[:8]
	ctr 		= Counter.new(64, nonce)
	aes_cipher	= AES.new(key, AES.MODE_CTR, counter=ctr)
	plaintext	= aes_cipher.decrypt(enc_input[8:])

	return plaintext