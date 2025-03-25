from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FEREN_KEY)
# Encrypting sensitive data
def encrypt_password(data: str) -> str:
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

# Decrypting sensitive data
def decrypt_password(encrypted_data: str) -> str:
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()
