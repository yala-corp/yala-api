from storages.backends.s3boto3 import S3Boto3Storage
from config import prod

class StaticStorage(S3Boto3Storage):
    location = prod.STATICFILES_LOCATION
    default_acl = prod.AWS_DEFAULT_ACL

class MediaStorage(S3Boto3Storage):
    location = prod.MEDIAFILES_LOCATION
    default_acl = prod.AWS_DEFAULT_ACL
    custom_domain = False
