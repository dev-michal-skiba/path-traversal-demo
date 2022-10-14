from io import StringIO
from os.path import basename, isabs

import paramiko
from django.conf import settings

from storage.models import SFTPCredentials


def _is_path_valid(path):
    return isabs(path) and '../' not in path and path[-4:] == '.pdf'


def _get_pdf_bytes_from_sftp_server(username, path, safe=True):
    remote_path = settings.SFTP_BASE_DIR + username + '/' + path
    if safe and not _is_path_valid(remote_path):
        return None

    private_key = SFTPCredentials.objects.last().private_key_string
    private_key = StringIO(private_key)
    private_key = paramiko.RSAKey.from_private_key(private_key)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=settings.SFTP_HOSTNAME, port=settings.SFTP_PORT,
        username=settings.SFTP_USERNAME, pkey=private_key
    )
    sftp_client = ssh_client.open_sftp()

    try:
        with sftp_client.open(remote_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None


def get_pdf_from_request(request, safe=True):
    path = request.GET.get('path', '')
    filename = basename(path)
    pdf_bytes = _get_pdf_bytes_from_sftp_server(
        username=request.user.username, path=path, safe=safe
    )
    return filename, pdf_bytes
