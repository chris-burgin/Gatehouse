try:
    from Crypto.Hash import SHA256
except ImportError:
    pass


class Security:

    # ENCRPYT
    def encrypt(self, value):
        h = SHA256.new()
        h.update(value)
        return str(h.hexdigest())
