from django.db.models.signals import post_save
from django.dispatch import receiver

from storage.models import SFTPFile
from storage.utils import create_mock_pdf


@receiver(post_save, sender=SFTPFile)
def create_profile(instance, created, **kwargs):
    if created and instance:
        create_mock_pdf(instance)
