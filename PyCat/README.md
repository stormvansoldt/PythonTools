# PyCat

My version of netcat, but written in Python. Requires Python 3.

**Usage:** ./pycat.py [-h] [-l] <HOST> <PORT>

**Positional arguments:**<br />
HOST: remote or local destination to connect/bind to<br />
PORT: port to connect to/listen on

**Optional arguments:**<br />
-h: show this help message and exit<br />
-l: listen for a connection (aka "server mode")

**Examples**<br />
./pycat.py 192.168.1.55 80<br />
./pycat.py -l 0.0.0.0 4444