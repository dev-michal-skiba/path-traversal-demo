from django import forms

from storage.encryptor import Encryptor
from storage.models import SFTPCredentials, SFTPFile


class SFTPCredentialsForm(forms.ModelForm):
    class Meta:
        model = SFTPCredentials
        fields = ('private_key',)

    def __init__(self, *args, **kwargs):
        super(SFTPCredentialsForm, self).__init__(*args, **kwargs)
        self.object_pk = None
        self.old_private_key = ''
        if hasattr(self, 'instance'):
            self.object_pk = self.instance.pk
            if self.instance.private_key:
                self.old_private_key = self.instance.private_key.strip()

    def clean_private_key(self):
        private_key = self.cleaned_data['private_key'].strip()
        if (
            not self.object_pk or
            self.object_pk and self.old_private_key != private_key
        ):
            encryptor = Encryptor()
            return encryptor.encrypt(private_key)
        return private_key


class FileForm(forms.ModelForm):
    class Meta:
        model = SFTPFile
        fields = ('month', 'year')

    def save(self, user):
        self.instance.user = user
        super(FileForm, self).save()
