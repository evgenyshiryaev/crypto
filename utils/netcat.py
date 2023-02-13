import socket

class Netcat:

    DEFAULT_LENGTH = 1024

    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))


    def read(self, length = DEFAULT_LENGTH):
        return self.socket.recv(length)


    def readText(self, length = DEFAULT_LENGTH):
        return self.read(length).decode()


    def readTextUntil(self, until):
        text = ''
        while not until in text:
            text += self.readText()
        return text


    def write(self, data):
        self.socket.send(data)
    

    def writeText(self, text):
        self.write(text.encode())


    def close(self):
        self.socket.close()
