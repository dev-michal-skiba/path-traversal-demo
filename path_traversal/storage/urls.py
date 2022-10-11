from django.urls import path

from storage.views import download_file_safe, download_file_unsafe


urlpatterns = [
    path('download/', download_file_safe, name='download-safe'),
    path('download/unsafe/', download_file_unsafe, name='download-unsafe'),
]
