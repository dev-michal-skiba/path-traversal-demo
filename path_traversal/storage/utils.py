from io import BytesIO, StringIO
from os.path import dirname, relpath

import paramiko
from django.conf import settings
from reportlab.pdfgen import canvas

from storage.models import SFTPCredentials


class PathTraversalException(Exception):
    pass


def _get_remote_path(username, filename, safe):
    remote_path = settings.SFTP_BASE_DIR + username + '/' + filename
    processed_path = relpath(remote_path, start=settings.SFTP_BASE_DIR)
    if safe and processed_path != username + '/' + filename:
        raise PathTraversalException
    return remote_path


def _get_pdf_bytes_from_sftp_server(remote_path):
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


def _save_pdf_bytes_on_sftp_server(pdf_bytes, remote_path):
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
        with sftp_client.open(remote_path, 'wb') as file:
            return file.write(pdf_bytes)
    except FileNotFoundError:
        sftp_client.mkdir(dirname(remote_path))
        with sftp_client.open(remote_path, 'wb') as file:
            return file.write(pdf_bytes)


def get_pdf_from_request(request, safe=True):
    filename = request.GET.get('filename', '')

    try:
        remote_path = _get_remote_path(
            username=request.user.username, filename=filename, safe=safe
        )
    except PathTraversalException:
        return filename, BytesIO()

    pdf_bytes = _get_pdf_bytes_from_sftp_server(remote_path)
    return filename, BytesIO(pdf_bytes)


def create_mock_pdf(file):
    remote_path = _get_remote_path(
        username=file.user.username, filename=file.filename
    )

    doc = canvas.Canvas(file.filename)
    doc.drawString(30, 750, 'Owner: {}'.format(file.user.username))
    doc.drawString(
        30, 735,
        'Mock invoice for {} {}'.format(file.month_human_readable, file.year)
    )

    _save_pdf_bytes_on_sftp_server(
        pdf_bytes=doc.getpdfdata(), remote_path=remote_path
    )
