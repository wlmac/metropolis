from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["localhost"]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_ROOT = "/app-static"

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_ROOT = "/app-media"
MEDIA_URL = "/media/"

try:
    with open(os.path.join(os.path.dirname(__file__), "local_settings2.py")) as f:
        exec(f.read(), globals())
except IOError:
    raise TypeError(
        "Please create a config file to override values in local_settings22.py"
    )
