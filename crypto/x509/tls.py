# https://github.com/google/google-ctf/tree/master/2023/crypto-mytls
# https://www.usenix.org/system/files/conference/woot15/woot15-paper-hlauschek.pdf


from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def load_crt(path):
    with open(path, 'rb') as crt_file:
        return x509.load_pem_x509_certificate(crt_file.read())


def load_key(path):
    with open(path, 'rb') as key_file:
        return serialization.load_pem_private_key(key_file.read(), None)


def verify(verify_crt, ca_crt):
    ca_crt.public_key().verify(verify_crt.signature, verify_crt.tbs_certificate_bytes,
                               padding.PKCS1v15(), verify_crt.signature_hash_algorithm)


def tls(server_key, server_crt, client_key, client_crt):
    server_secret = server_key.exchange(ec.ECDH(), client_crt.public_key())
    client_secret = client_key.exchange(ec.ECDH(), server_crt.public_key())
    assert server_secret == client_secret

    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=b'SaltyMcSaltFace', info=b'mytls')
    return hkdf.derive(server_secret)


if __name__ == '__main__':
    _ca_crt = load_crt('ca-crt.pem')
    verify(_ca_crt, _ca_crt)  # self-signed

    _server_crt = load_crt('server-ecdhcert.pem')
    verify(_server_crt, _ca_crt)  # CA signed
    _server_key = load_key('server-ecdhkey.pem')

    _client_crt = load_crt('client-ecdhcert.pem')
    verify(_client_crt, _ca_crt)  # CA signed
    _client_key = load_key('client-ecdhkey.pem')

    tls(_server_key, _server_crt, _client_key, _client_crt)
