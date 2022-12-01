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


def gcd(a, b):
    return gcd(b, a % b) if b != 0 else a


x = 0
y = 0

def gcdExt(a, b):
    global x
    global y

    if a == 0:
        x = 0
        y = 1
        return b

    d = gcdExt(b % a, a)

    xVal = y - b // a * x
    yVal = x

    x = xVal
    y = yVal

    return d


def find_dec(suffix):
    global x
    global y

    a = pow(10, len(suffix))
    b = -pow(16, len(suffix))
    c = int(suffix, 16) - int(suffix)
    print('eq', a, b, c)

    x = 0
    y = 0
    g = gcdExt(a, -b)
    print(g, x, y)

    mul = c // g
    x *= mul
    y *= mul
    if a < 0:
        x *= -1
    if b < 0:
        y *= -1
    
    if x < 0:
        inc = abs(b) // g
        count = abs(x) // inc
        x += (count + 1) * inc
    
    return (pow(10, len(suffix)) * x + int(suffix))


nc = Netcat('109.233.56.93', 20019)

print(nc.read())

for ii in range(1, 16):
    print(nc.read())

    data = nc.read().decode("utf-8")
    print(data)
    
    i = data.index('ends in')
    suffix = data[i + 8 : len(data) - 2]
    print(suffix)
    x = 0
    y = 0
    dec = find_dec(suffix) 
    print(dec)
    
    data = str(dec) + '\n'
    
    nc.write(data.encode('utf-8'))

print(nc.read())
print(nc.read())
print(nc.read())

nc.close()
