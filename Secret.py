from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Secret_Handshake:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.private_key = self.key.export_key('PEM')
        self.public_key = self.key.publickey().exportKey('PEM')
        #print(self.private_key)
    def network_key(self):
        return self.private_key

    def Encrypt(self, plain_msg):
        msg = str.encode(plain_msg)
        self.rsa_public_key = RSA.importKey(self.public_key)
        self.rsa_public_key = PKCS1_OAEP.new(self.rsa_public_key)
        self.encrypt = self.rsa_public_key.encrypt(msg)
        return self.encrypt

    def Decrypt(self, exchanged_key, encoded_msg):
        self.s_private_key = RSA.importKey(exchanged_key)
        self.s_private_key = PKCS1_OAEP.new(self.s_private_key)
        self.decrypt = self.s_private_key.decrypt(encoded_msg)
        return self.decrypt