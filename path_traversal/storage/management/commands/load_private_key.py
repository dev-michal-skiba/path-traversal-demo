from django.core.management.base import BaseCommand

from storage.models import SFTPCredentials


class Command(BaseCommand):
    help = 'Loads private key to database'

    def add_arguments(self, parser):
        parser.add_argument('--private-key', type=str)

    def handle(self, *args, **options):
        private_key = options.get('private_key')
        if private_key:
            SFTPCredentials.objects.create(private_key=private_key)
