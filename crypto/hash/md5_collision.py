# https://github.com/cr-marcstevens/hashclash
# https://github.com/brimstone/fastcoll

from hashlib import md5
import random

M0_0 = bytes.fromhex('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2')
M0_1 = bytes.fromhex('4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2')
M1_0 = bytes.fromhex('0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef')
M1_1 = bytes.fromhex('0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef')
assert md5(M0_0).hexdigest() == md5(M0_1).hexdigest()
assert md5(M1_0).hexdigest() == md5(M1_1).hexdigest()

m = random.randbytes(7)
assert md5(M0_0 + m).hexdigest() == md5(M0_1 + m).hexdigest()
