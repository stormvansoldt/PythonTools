# Scripts

A small collection of network-based tools written in Python. I am using this to both gain a better understanding of low-level networking concepts in a network security context, as well as to simply increase my own personal toolbox to get away from the "script kiddie" life :). Inspiration for this repo came from the book "Black Hat Python: Python Programming for Hackers and Pentesters" by Justin Seitz. 

Please note that all testing for these scripts was done using Python 3.6.2. I cannot guarantee that all (or any, for that matter) of these scripts will work with Python 2. I may add compatibility someday, but today is not that day.



*DISCLAIMER: I do not condone using these, or any scripts/programs/whatever for any illegal activity whatsoever. All testing for these scripts was done in an environment that either I controlled, or had explicit permission from the admin/owner to perform testing on. Don't hack shit that isn't yours.*

## PyCat

PyCat is basically what it sounds like - a clone of the popular tool netcat. My main goals for this project have nearly been completed at the time of updating this README, which was to gain a better understanding of how low-level networking sockets work. This isn't a completely fleshed out remake (yet(?)), but does support basic server/client features of netcat. Usage and examples can be found in the README in the PyCat folder.

## PyDump

A TCP proxy that allows us to intercept all TCP traffic to and from a remote connection. This script will take the data in-transit, and print both the ASCII and hex representations of said data to the console. Just like the other scripts, usage and examples can be found in the README of the PyDump folder.

