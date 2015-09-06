try:
    from Crypto.Hash import SHA256
except ImportError:
    pass


class Security:

    # Encrypt
    def encrypt(self, value):
        h = SHA256.new()
        h.update(value)
        return str(h.hexdigest())

    # Check Password Strength
    def passwordStrength(self, password):
        if len(password) > 5:
            if any(char.isdigit() for char in password):
                return True
        return False

    # Check Username
    def usernameStrength(self, username):
        if len(username) > 2:
            return True
        return False
