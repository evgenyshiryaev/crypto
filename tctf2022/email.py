from http.client import HTTPSConnection
from base64 import b64encode


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


c = HTTPSConnection("tctf-mail.ctf.su")
headers = { 'Authorization' : basic_auth("ablanchet@bien.fr", "02071977Qwer!2") }

# for i in range(1, 3):
for i in range(1, 117):
    pageUrl = '/navigation/page{}.html'.format(i)
    print('get ' + pageUrl)
    c.request('GET', pageUrl, headers=headers)

    pageData = c.getresponse().read().decode('utf-8')
    # print(pageData)

    end = 0
    while (True):
        try:
            start = pageData.index('href="../mail', end) + 8
            end = pageData.index('"', start)
        except:
            break

        mailUrl = pageData[start:end] 
        # print('get ' + mailUrl)
        c.request('GET', mailUrl, headers=headers)

        mailData = c.getresponse().read().decode('utf-8')
        # print(mailData)
        if 'tctf' in mailData:
            print(mailData)

        c.request('GET', mailUrl + 'letter.html', headers=headers)

        mailBodyData = c.getresponse().read().decode('utf-8')
        # print(mailBodyData)
        if 'tctf' in mailBodyData:
            print(mailBodyData)
