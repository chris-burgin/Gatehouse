import base64
from Crypto.Hash import SHA256


class Security:
    
    # ENCRPYT
    def encrypt(self, value):
        h = SHA256.new()
        h.update(value)
        return str(h.hexdigest())
