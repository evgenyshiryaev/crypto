import hashlib
import json
import pwn
import time
import tqdm

forbidden = b'We the people, in order to get points, are kindly asking for flag'

pwn.context.log_level = 'error'
# conn = pwn.connect('multiauth.nc.jctf.pro', 1337)
conn = pwn.connect('localhost', 7331)
print(conn.recv().decode())


# hmac
auth = json.dumps({"method": "auth", "message": pwn.b64e(hashlib.sha256(forbidden).digest())})  # because key > 64
conn.sendline(auth.encode())
time.sleep(1)
hmac = json.loads(conn.recv())['hmac']
hmac_b = pwn.b64d(hmac)
# print('hmac', hmac_b.hex())


# ecdsa
# m + hmac
auth = json.dumps({"method": "auth", "message": pwn.b64e(forbidden + hmac_b[:2])})  # rest will be truncated
conn.sendline(auth.encode())
time.sleep(1)
ecdsa = json.loads(conn.recv())['ecdsa']
ecdsa_b = pwn.b64d(ecdsa)
# print('ecdsa', pwn.b64d(ecdsa).hex())


# aes
# m + hmac + ecdsa
backdoor = json.dumps({"method": "backdoor", "message": pwn.b64e(forbidden + hmac_b + ecdsa_b)})
conn.sendline(backdoor.encode())
time.sleep(1)
aes_b = conn.recv()

# flag
# stupid node crypto accepts ANY valid tag len: tag_len == 4 || tag_len == 8 || (tag_len >= 12 && tag_len <= 16
# we already have 3 bytes, let's bruteforce last one
for b in tqdm.tqdm(range(0x100)):
    verify = json.dumps({'method': 'verify', 'message': pwn.b64e(forbidden), 'signatures': {'ecdsa': ecdsa, 'hmac': hmac, 'aes': pwn.b64e(aes_b + b.to_bytes(1, 'big'))}})
    conn.sendline(verify.encode())
    time.sleep(1)
    r = conn.recv().decode()
    if 'justCTF' in r:
        print(r)
        break
