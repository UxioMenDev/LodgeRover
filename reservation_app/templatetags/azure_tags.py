# Template tags for Azure storage SAS URLs
from django import template
from django.conf import settings
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
import logging

register = template.Library()
logger = logging.getLogger(__name__)


@register.simple_tag
def azure_media_url(file_path, expire_hours=1):
    """
    Generate a secure URL with SAS token for media files
    Usage: {% azure_media_url "path/to/file.jpg" %}
    """
    if not hasattr(settings, 'AZURE_ACCOUNT_NAME') or not settings.AZURE_ACCOUNT_NAME:
        return file_path
        
    try:
        # Generate SAS token
        sas_token = generate_blob_sas(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY,
            container_name=settings.AZURE_CONTAINER,
            blob_name=f"media/{file_path}",
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=expire_hours)
        )
        
        # Build URL with SAS token
        blob_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/media/{file_path}"
        return f"{blob_url}?{sas_token}"
        
    except Exception as e:
        logger.error(f"Error generating SAS token for {file_path}: {e}")
        # Fallback to MEDIA_URL + file_path
        return f"{settings.MEDIA_URL}{file_path}"


@register.simple_tag
def azure_static_url(file_path, expire_hours=24):
    """
    Generate a secure URL with SAS token for static files
    Usage: {% azure_static_url "css/style.css" %}
    """
    if not hasattr(settings, 'AZURE_ACCOUNT_NAME') or not settings.AZURE_ACCOUNT_NAME:
        return file_path
        
    try:
        # Generate SAS token
        sas_token = generate_blob_sas(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY,
            container_name=settings.AZURE_CONTAINER,
            blob_name=f"static/{file_path}",
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=expire_hours)
        )
        
        # Build URL with SAS token
        blob_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{settings.AZURE_CONTAINER}/static/{file_path}"
        return f"{blob_url}?{sas_token}"
        
    except Exception as e:
        logger.error(f"Error generating SAS token for static file {file_path}: {e}")
        # Fallback to STATIC_URL + file_path
        return f"{settings.STATIC_URL}{file_path}"
