from django.conf import settings

# AWS S3 Storage classes - only used when AWS is enabled
if hasattr(settings, 'AWS_STORAGE_BUCKET_NAME') and settings.AWS_STORAGE_BUCKET_NAME:
    from storages.backends.s3boto3 import S3Boto3Storage

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
else:
    # Dummy classes when AWS is not used (to avoid import errors)
    class MediaStorage:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("AWS S3 storage not configured. Use Azure storage instead.")
    
    class StaticStorage:
        def __init__(self, *args, **kwargs):
            raise RuntimeError("AWS S3 storage not configured. Use Azure storage instead.")
