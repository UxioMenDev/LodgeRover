from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'media'
    default_acl = None  # No ACLs - use bucket policy for public access
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'static'
    default_acl = None  # No ACLs - use bucket policy for public access
    file_overwrite = True
