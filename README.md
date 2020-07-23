# Entangled v1.0
==========================================================================<br/>
This is a very simple Remote administration tool for testing purposes only.<br/>
Will work on windows or linux, but linux is the perferd current platform.<br/>


Installation<br/>
================================================================================<br/>
These are pyscripts that require python2. Please run scripts in python2 enviorments.

Gettting Started <br/>
========================================================= <br/>

usage on server:  <br/>
python2.7 server.py <br/>

current commands with LP: <br/> 
list = list current sessions <br/> 
session = select sessopn <br/>
exit = kill server <br/> 

Should display: <br/> 

Waiting for connections .... <br/> 
Entangle:  <br/> 


When a connection is made <br/> 
======================================================================================== <br/> 
Waiting for connections .... <br/>
Entangle: **** 127.0.0.1 Has Connected **** <br/>


List command = list all current sessions <br/> 
=========================================== <br/>
Entangle: list <br/> 
Session 0 ----> ('127.0.0.1', 52883) <br/> 
Session 1 ----> ('192.168.159.133', 38308) <br/> 
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
