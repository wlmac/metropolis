import os

import os.path

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]

STATIC_ROOT = ''
BANNER2=''
STATIC_URL = '/static/'

STATICFILES_DIRS = ( os.path.join('static'), )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ["*"]
DEBUG = True

RECAPTCHA_PUBLIC_KEY = '6LdlaxcaAAAAAOfjhmSj9omG82WU2gAmsqNIV97U'
RECAPTCHA_PRIVATE_KEY = '6LdlaxcaAAAAADZ6FKglAYsjTD9jl_hrUlsVltLi'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_TIMEZONE = 'America/Toronto'

MEDIA_URL = '/media/'
MEDIA_URL = 'http://127.0.0.1:8080/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tmp')

DEFAULT_FROM_EMAIL = 'hello@maclyonsden.com'
SERVER_EMAIL = 'hello@maclyonsden.com'

MAPBOX_APIKEY = 'pk.eyJ1IjoibmlraXN1IiwiYSI6ImNrc3A3c2FieTAwM3kybnA3anNjY2c3MXMifQ.T_8vAyTc4PMuGUC23vIOhA'

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
