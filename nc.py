import socket
 
class Netcat:
    def __init__(self, ip, port):

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length = 1024):
        return self.socket.recv(length)
 
    def read_until(self, data):
        while not data in self.buff:
            self.buff += self.socket.recv(1024)
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
        return rval
 
    def write(self, data):
        self.socket.send(data)
    
    def close(self):
        self.socket.close()

nc = Netcat('109.233.56.93', 20019)

print(nc.read(10000))
print(nc.read(10000))


# get to the prompt
# nc.read_until('>')

# start a new note
# nc.write('new' + '\n')
# nc.read_until('>')

# set note 0 with the payload
# nc.write('set' + '\n')
# nc.read_until('id:')
