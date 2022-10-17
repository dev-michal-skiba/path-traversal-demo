from django.conf import settings
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


class SFTPFile(models.Model):
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )

    MONTH_MAP = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december',
    }

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()

    @property
    def filename(self):
        return '{}_{}.pdf'.format(self.month_human_readable, self.year)

    @property
    def month_human_readable(self):
        return self.MONTH_MAP[self.month]

    def __str__(self):
        return '{} - {}'.format(self.user, self.filename)

    class Meta:
        unique_together = ('user', 'month', 'year')
