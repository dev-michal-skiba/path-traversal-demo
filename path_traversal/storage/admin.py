from django.contrib import admin

from storage.forms import SFTPCredentialsForm
from storage.models import SFTPCredentials, SFTPFile


@admin.register(SFTPCredentials)
class SFTPSettingsAdmin(admin.ModelAdmin):
    form = SFTPCredentialsForm


admin.site.register(SFTPFile)
