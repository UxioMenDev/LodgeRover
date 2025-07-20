# Use default django-storages Azure backend
# This is a simplified approach that uses the default AzureStorage class

from django.conf import settings
from storages.backends.azure_storage import AzureStorage


# For media files
class AzureMediaStorage(AzureStorage):
    location = 'media'
    file_overwrite = False


# For static files  
class AzureStaticStorage(AzureStorage):
    location = 'static'
    file_overwrite = True
