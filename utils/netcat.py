import socket


# see https://docs.pwntools.com/en/stable/intro.html
# use pwn.remote
# context.log_level = 'error'
class NetcatDeprecated:

    DEFAULT_LENGTH = 1024

    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length=DEFAULT_LENGTH):
        return self.socket.recv(length)

    def read_text(self, length=DEFAULT_LENGTH):
        return self.read(length).decode()

    def read_text_until(self, until):
        text = ''
        while not until in text:
            text += self.read_text()
        return text

    def write(self, data):
        self.socket.send(data)

    def write_text(self, text):
        self.write(text.encode())

    def close(self):
        self.socket.close()
