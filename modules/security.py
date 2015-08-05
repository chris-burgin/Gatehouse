try:
    from Crypto.Hash import SHA256
except ImportError:
    import sys
    sys.path.append('/[mypath]/anaconda/lib/python2.7/site-packages')
    from Crypto.Hash import SHA256 # requires PyCrypto


class Security:

    # ENCRPYT
    def encrypt(self, value):
        h = SHA256.new()
        h.update(value)
        return str(h.hexdigest())
