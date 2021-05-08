import socket
import pickle

#connecting to server
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 127.0.0.1- the ip of the current used computer
        # 192.168.1.13- the ip of my computer
        self.server = "127.0.0.1"
        # same port number as the port number in the server file
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        # put the connect in try- in case it won't be able to connect
        try:
            self.client.connect(self.addr)
            # reciving the players number 0 or 1
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)