import coincurve
import json
import pwn

# openssl ecparam -genkey -name secp256r1 -noout -out private.pem
# priv = coincurve.PrivateKey.from_hex('4e125729e4c7ab94625a88bd43009e3ec82c4bcce1877b9e2969a00954cce357')
# openssl ec -in private.pem -text -noout -conv_form compressed
# openssl ec -in private.pem -text -noout -conv_form uncompressed
# openssl ec -in private.pem -text -noout -conv_form hybrid
# pub_c = '022a1a323d6a2e955ccd51814b18cf9c38f12e56f2d503b2e5da87e5b42e2f9d97'
# pub_u = '042a1a323d6a2e955ccd51814b18cf9c38f12e56f2d503b2e5da87e5b42e2f9d97faf2c160af9a53940cb7f2d9d4793a74db980d20a7ef47f8b0b91ff59ef9153c'
# pub_h = '062a1a323d6a2e955ccd51814b18cf9c38f12e56f2d503b2e5da87e5b42e2f9d97faf2c160af9a53940cb7f2d9d4793a74db980d20a7ef47f8b0b91ff59ef9153c'

# or

priv = coincurve.PrivateKey()

pub = priv.public_key
pub_c = pub.format().hex()
pub_u = pub.format(False).hex()
pub_h = '06' + pub_u[2:]
# print(pub_c)
# print(pub_u)
# print(pub_h)

m = b'get_flag'
sign = priv.sign(m).hex()
# print(sign)

enroll = json.dumps({'method': 'enroll', 'pubkey': pub_c})
get_flag = json.dumps({'method': 'get_flag', 'pubkeys': [pub_c, pub_u, pub_h], 'signatures': [sign] * 3})
# print(enroll)
# print(get_flag)

conn = pwn.remote('vaulted.nc.jctf.pro', 1337)
print(conn.recv().decode())
conn.sendline(enroll.encode())
print(conn.recv().decode())
conn.sendline(get_flag.encode())
print(conn.recv().decode())
