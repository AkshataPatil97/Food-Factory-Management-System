from django.contrib.auth.hashers import make_password, check_password

def encrypt_password(password):
    """Encrypts (hashes) the password"""
    return make_password(password)

def verify_password(password, hashed_password):
    """Verifies if the password matches the hashed password"""
    return check_password(password, hashed_password)
