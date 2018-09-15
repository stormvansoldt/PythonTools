#!/usr/bin/python3

import sys
import socket
import PyRSA
from Crypto.Random import get_random_bytes

'''
TODO:
 - Test with an external module (probably PyCat or something like that)

This module has the functions needed to handle the initialization of the
encryption libray. Here is a simple walkthrough of the init process:

 1. Ensure a valid connection between the server and client.
 2. After connection is validated, the client creates the RSA keypair and
    sends the public key to the server.
 3. The server accepts the public key from the client.
 4. The server generates a random sequence of 16 bytes to be used as the
    AES encryption key for the remainder of the session.
 5. Server encrypts the session key using the client's public RSA key
 6. Encrypted session key is sent back to the client.
 7. Client decrypts the AES key using the private RSA key.
 8. Both ends of the connection now have the session key, and the encrypted
    communication can begin.

'''


def server_handler(conn):
    '''
    Receive an RSA public key from the client, generate a 128-bit AES session
    key, encrypt it with the public key, then send it back to the client.

    Keyword arguments:
    conn -- socket object representing the connection to the client.

    Returns:
     session_key -- bytestring of the AES key
    '''
    if not conn:
        print('[!] Error! Invalid connection was passed')
        return 1

    print('[ ] Waiting to receive client\'s public key...')
    pub_key = conn.recv(2048)
    print('[*] Received public key!')

    print('[ ] Generating AES session key and encrypting it with the public '
          'RSA key...')
    session_key = get_random_bytes(16)

    print('[*] Sending AES key to client')
    conn.sendall(PyRSA.rsa_encrypt(session_key, pub_key))

    return session_key


def client_handler(conn):
    '''
    Generate a 2048-bit RSA keypair, send the public key to the server,
    receive the encrypted AES session key as a response, then decrypt it
    using the private RSA key.

    Keyword arguments:
     conn -- socket object representing the connection to the server.

    Returns:
     session_key -- bytestring of the AES key
    '''
    if not conn:
        print('[!] Error! Invalid connection was provided')
        return 1

    (pub_key, priv_key) = PyRSA.generate_keypair()

    print('[ ] Sending public key to the server...')
    conn.sendall(pub_key)

    print('[ ] Waiting to receive the encrypted session key...')
    enc_session_key = conn.recv(2048)

    print('[*] Received encrypted session key!')
    session_key = PyRSA.rsa_decrypt(enc_session_key, priv_key)

    print('[*] Decrypted the session key!')

    return session_key


def main():
    arg = sys.argv[1]

    if arg == 'l':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', 32123))
        sock.listen(1)
        conn, addr = sock.accept()
        print(server_handler(conn))
        conn.close()
        sock.close()

    elif arg == 'c':
        conn = socket.create_connection(('127.0.0.1', 32123))
        print(client_handler(conn))
        conn.close()
    else:
        print('try again asshole')


if __name__ == '__main__':
    main()
