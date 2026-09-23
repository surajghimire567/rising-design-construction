from .base import *  # noqa: F403
from django.core.exceptions import ImproperlyConfigured

if DEBUG:
    raise ImproperlyConfigured("Production refuses to start with DEBUG=True.")
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("Set ALLOWED_HOSTS to the exact hostnames for this site.")
if SECRET_KEY == "dev-only-do-not-use-in-production-change-this-key" or len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("Set a generated SECRET_KEY of at least 50 characters.")
if not DATABASES["default"].get("ENGINE", "").endswith("postgresql"):
    raise ImproperlyConfigured("Production requires PostgreSQL via DATABASE_URL.")
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("Set CSRF_TRUSTED_ORIGINS to the site's full https:// origins.")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

USE_R2 = env.bool("USE_R2", default=False)
if not USE_R2:
    raise ImproperlyConfigured("Production requires USE_R2=True; Render's local filesystem is ephemeral.")
R2_ACCOUNT_ID = env("R2_ACCOUNT_ID", default="")
R2_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID", default="")
R2_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY", default="")
R2_PUBLIC_BUCKET = env("R2_PUBLIC_BUCKET", default="")
R2_PRIVATE_BUCKET = env("R2_PRIVATE_BUCKET", default="")
R2_PUBLIC_CUSTOM_DOMAIN = env("R2_PUBLIC_CUSTOM_DOMAIN", default="")
if not all([R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_PUBLIC_BUCKET, R2_PRIVATE_BUCKET, R2_PUBLIC_CUSTOM_DOMAIN]):
    raise ImproperlyConfigured("Set all R2 credentials, bucket names, and public custom domain before production startup.")

R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
STORAGES = {
    **STORAGES,
    "public_media": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": R2_ACCESS_KEY_ID,
            "secret_key": R2_SECRET_ACCESS_KEY,
            "bucket_name": R2_PUBLIC_BUCKET,
            "endpoint_url": R2_ENDPOINT,
            "region_name": "auto",
            "custom_domain": R2_PUBLIC_CUSTOM_DOMAIN,
            "querystring_auth": False,
            "file_overwrite": False,
            "default_acl": None,
            "location": "media",
            "object_parameters": {"CacheControl": "public, max-age=3600"},
        },
    },
    "private_uploads": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": R2_ACCESS_KEY_ID,
            "secret_key": R2_SECRET_ACCESS_KEY,
            "bucket_name": R2_PRIVATE_BUCKET,
            "endpoint_url": R2_ENDPOINT,
            "region_name": "auto",
            "querystring_auth": True,
            "querystring_expire": 300,
            "file_overwrite": False,
            "default_acl": None,
            "location": "inquiries",
        },
    },
}
