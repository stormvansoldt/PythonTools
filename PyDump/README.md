# PyDump

Creates a simple man-in-the-middle so we can proxy any TCP requests to or from a remote host.

**Usage:** ./pydump.py [-h] PORT TARGET

**Positional arguments:**<br />
PORT: local port to bind the listener to<br />
TARGET: remote host to connect to in the form of (IP:PORT)

**Optional arguments:**<br />
-h: show this help message and exit<br />

**Examples:**<br />
./pydump.py 9001 192.168.0.35:22

TODO:
- Refactor code