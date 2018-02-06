# PyCat

My version of netcat, but written in Python. Requires Python 3.

**Usage:** ./pycat.py [-h] [-l] HOST PORT

Simple copy of netcat written in Python.

positional arguments:
  HOST        remote or local destination to connect/bind to
  PORT        port to connect to/listen on

optional arguments:
  -h, --help  show this help message and exit
  -l          listen for a connection (aka "server mode")

**Examples**
./pycat.py 192.168.1.55 80
./pycat.py -l 0.0.0.0 4444