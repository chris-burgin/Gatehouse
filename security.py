import base64
from Crypto.Hash import SHA256


class Security:
    def __init__(self):
        print('Security Created')

    # ENCRPYT
    def encrypt(self, value):
        h = SHA256.new()
        h.update(value)
        return h.hexdigest()
