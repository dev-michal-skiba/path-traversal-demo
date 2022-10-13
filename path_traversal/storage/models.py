from django.db import models

from storage.encryptor import Encryptor


class SFTPCredentialsManager(models.Manager):
    def create(self, private_key):
        encryptor = Encryptor()
        encrypted_private_key = encryptor.encrypt(private_key)
        super(SFTPCredentialsManager, self).create(
            private_key=encrypted_private_key
        )


class SFTPCredentials(models.Model):
    private_key = models.TextField()

    class Meta:
        verbose_name = "SFTP Credentials"
        verbose_name_plural = "SFTP Credentials"

    @property
    def private_key_string(self):
        encryptor = Encryptor()
        return encryptor.decrypt(self.private_key)

    objects = SFTPCredentialsManager()
