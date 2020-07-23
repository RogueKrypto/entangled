# Entangled v1.0
====================================================
This is a very simple Remote administration tool for testing purposes only.
Will work on windows or linux, but linux is the perferd current platform.


Installation
=======================================================
These are pyscripts that require python2. Please run scripts in python2 enviorments.

Gettting Started
=========================================================

usage on server: 
python2.7 server.py

current commands with LP:
list = list current sessions
session = select sessopn
exit = kill server

Should display:

Waiting for connections ....
Entangle: 


When a connection is made
========================================================================================
Waiting for connections ....
Entangle: **** 127.0.0.1 Has Connected ****


List command = list all current sessions
===========================================
Entangle: list
Session 0 ----> ('127.0.0.1', 52883)
Session 1 ----> ('192.168.159.133', 38308)
Entangle: 



Session Command = select session
=========================================================================================
Entangle: list
Session 0 ----> ('127.0.0.1', 52883)
Session 1 ----> ('192.168.159.133', 38308)
Entangle: session 0
Session~# 


Current commands with session:
once connected you can run regular commands or use built in commands

cd = change directory
upload = upload file
download = download file
detach = detach current session
quit = kill current session

client
====================================
python2.7 client.py
