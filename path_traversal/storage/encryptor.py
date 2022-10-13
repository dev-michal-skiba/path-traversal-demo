import base64

from django.conf import settings

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryptor:

    def __init__(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), length=32, salt=settings.SFTP_SALT,
            iterations=390000
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.SFTP_SECRET))
        self.fernet = Fernet(key)

    def encrypt(self, value):
        value = str.encode(value)
        return self.fernet.encrypt(value).decode()

    def decrypt(self, value):
        value = str.encode(value)
        return self.fernet.decrypt(value).decode()
