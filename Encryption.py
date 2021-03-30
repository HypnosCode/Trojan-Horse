import pickle


class titan:
    def __init__(self):
        self.key = 128

    def encryption(self, msg):
        encrypted = ''
        for enc in msg:
            text = ord(enc)
            text = text+self.key
            text = pickle.dumps(text)
            text = str(text)+'/'
            encrypted += text
        return encrypted

    def decryption(self, msg):
        load = msg.split('/')
        #load = load.pop()
        print(load)
        decrypted = ''
        for enc in load:
            text = pickle.loads(enc)
            text = int(text)-self.key
            text = chr(text)
            decrypted += text
        return decrypted


obj = titan()
a = obj.encryption("prayag")
print(a)
print(obj.decryption(a))
