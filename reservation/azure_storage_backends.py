# Azure Storage backends for Django with SAS token support
from storages.backends.azure_storage import AzureStorage
from django.conf import settings
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import logging

logger = logging.getLogger(__name__)


class AzureMediaStorage(AzureStorage):
    """
    Storage for media files in Azure Blob Storage with SAS token authentication
    """
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    location = 'media'
    overwrite_files = getattr(settings, 'AZURE_OVERWRITE_FILES', False)
    expiration_secs = getattr(settings, 'AZURE_URL_EXPIRATION_SECS', 3600)
    
    def url(self, name, expire=None):
        """
        Generate a URL with SAS token for secure access
        """
        if expire is None:
            expire = self.expiration_secs
            
        try:
            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                account_key=self.account_key,
                container_name=self.azure_container,
                blob_name=f"{self.location}/{name}" if self.location else name,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(seconds=expire)
            )
            
            # Build URL with SAS token
            blob_url = f"https://{self.account_name}.blob.core.windows.net/{self.azure_container}/{self.location}/{name}"
            return f"{blob_url}?{sas_token}"
            
        except Exception as e:
            logger.error(f"Error generating SAS token for {name}: {e}")
            # Fallback to standard URL without SAS token
            return super().url(name)


class AzureStaticStorage(AzureStorage):
    """
    Storage for static files in Azure Blob Storage with SAS token authentication
    """
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.AZURE_CONTAINER
    location = 'static'
    overwrite_files = True  # Static files can be overwritten
    expiration_secs = getattr(settings, 'AZURE_URL_EXPIRATION_SECS', 3600)
    
    def url(self, name, expire=None):
        """
        Generate a URL with SAS token for secure access to static files
        """
        if expire is None:
            expire = self.expiration_secs
            
        try:
            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=self.account_name,
                account_key=self.account_key,
                container_name=self.azure_container,
                blob_name=f"{self.location}/{name}" if self.location else name,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(seconds=expire)
            )
            
            # Build URL with SAS token
            blob_url = f"https://{self.account_name}.blob.core.windows.net/{self.azure_container}/{self.location}/{name}"
            return f"{blob_url}?{sas_token}"
            
        except Exception as e:
            logger.error(f"Error generating SAS token for static file {name}: {e}")
            # Fallback to standard URL without SAS token
            return super().url(name)
