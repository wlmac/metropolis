from pathlib import Path

_using_docker_config = True  # intended for allow changing config *in dev*

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["localhost"]

STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"  # decapitated
)
STATIC_ROOT = "/app-public"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"  # decapitated
MEDIA_ROOT = "/app-media"
MEDIA_URL = "/media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "metropolis_db",
        "USER": "metropolis_user",
        "PASSWORD": "changeme_metropolis_password",  # CHANGE IN PROD
        "HOST": "postgres",
        "PORT": "",
    }
}

CELERY_BROKER_URL = "redis://redis:6379"

try:
    with open(os.path.join(os.path.dirname(__file__), "local_settings2.py")) as f:
        exec(f.read(), globals())
except IOError:
    raise TypeError(
        "Please create a config file to override values in local_settings2.py"
    )
