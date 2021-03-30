import socket
from Secret import Secret_Handshake
from base64 import *

class Encrypted_Network(object):
    """
    This is a socket modified class using different encryptation
    """
    def __init__(self, IP='', PORT=4983):
        self.IP = IP
        self.PORT = PORT
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setTCP(self, l_num):
        self.tcp_sock.bind((self.IP, self.PORT))
        self.tcp_sock.listen(l_num)

    def connectTcp(self):
        self.tcp_sock.connect((self.IP, self.PORT))

    def Accept_Connection(self):
        self.conn, self.addr = self.tcp_sock.accept()
        return (self.conn, self.addr)

    def Secure_Connnect(self):
        self.obj = Secret_Handshake()
        self.private_key = self.obj.network_key()
        #print(len(self.private_key))
        #self.encoded_key = b64encode(self.private_key)

    def Exchange_Key(self):
        self.conn.sendall(self.private_key)

    def Recv_Key(self):
        Eslave_private_key = self.conn.recv(2048)
        #slave_private_key = b64decode(Eslave_private_key)
        return Eslave_private_key

    def Exchange_Key_Sock(self):
        self.tcp_sock.sendall(self.private_key)

    def Recv_Key_Sock(self):
        slave_key_tcp = self.tcp_sock.recv(2048)
        #slave_key_tcp = b64decode(slave_key_tcp)
        return slave_key_tcp

    def Send_Message(self, msg):
        encrypted = self.obj.Encrypt(msg)
        self.conn.send(encrypted)

    def Recv_Message(self, key):
        unrefined  = self.conn.recv(2048)
        processed = self.obj.Decrypt(key, unrefined)
        return processed

    def Send_Message_Sock(self, plain_text):
        encrypted = self.obj.Encrypt(plain_text)
        self.tcp_sock.send(encrypted)

    def Recv_Message_Sock(self, key):
        unrefined = self.tcp_sock.recv(2048)
        processed = self.obj.Decrypt(key, unrefined)
        return processed
