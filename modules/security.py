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

    def passwordStrength(self, password):
        if len(password) > 5:
            if any(char.isdigit() for char in password):
                return True
        return False

    def usernameStrength(self, username):
        if len(username) > 2:
            return True
        return False
