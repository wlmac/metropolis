import os
from datetime import datetime, timedelta
from typing import Dict, List

from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "Change me"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.redirects",
    "core",
    "allauth",
    "allauth.account",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "martor",
    "django_select2",
    "pwa",
    "oauth2_provider",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.flatpages.middleware.FlatpageFallbackMiddleware",
    "core.middleware.TimezoneMiddleware",
    "core.middleware.CustomRedirectFallbackTemporaryMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
]

ROOT_URLCONF = "metropolis.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "metropolis.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Auth settings

AUTH_USER_MODEL = "core.User"

# Media settings

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Timetable settings

TERM_GRACE_PERIOD = timedelta(weeks=2)

TIMETABLE_FORMATS = {
    "pre-2020": {
        "schedules": {
            "default": [
                {
                    "description": {
                        "time": "08:45 am - 10:05 am",
                        "course": "Period 1",
                    },
                    "time": [[8, 45], [10, 5]],
                    "position": [{1}, {1}],
                },
                {
                    "description": {
                        "time": "10:15 am - 11:30 am",
                        "course": "Period 2",
                    },
                    "time": [[10, 15], [11, 30]],
                    "position": [{2}, {2}],
                },
                {
                    "description": {
                        "time": "12:30 pm - 01:45 pm",
                        "course": "Period 3",
                    },
                    "time": [[12, 30], [13, 45]],
                    "position": [{3}, {4}],
                },
                {
                    "description": {
                        "time": "01:50 pm - 03:05 pm",
                        "course": "Period 4",
                    },
                    "time": [[13, 50], [15, 5]],
                    "position": [{4}, {3}],
                },
            ]
        },
        "courses": 4,
        "positions": {1, 2, 3, 4},
        "cycle": {
            "length": 2,
            "duration": "day",
        },
        "question": {
            "prompt": "Your Nth course on day 1 is this course. N = ?",
            "choices": [
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
            ],
        },
    },
    "covid": {
        "schedules": {
            "default": [
                {
                    "description": {
                        "time": "08:45 am - 12:30 pm (In person)",
                        "course": "Morning Class",
                    },
                    "time": [[8, 45], [12, 30]],
                    "position": [{1}, {2}, {3}, {4}],
                },
                {
                    "description": {
                        "time": "08:45 am - 12:30 pm (At home)",
                        "course": "Morning Class",
                    },
                    "time": [[8, 45], [12, 30]],
                    "position": [{2}, {1}, {4}, {3}],
                },
                {
                    "description": {
                        "time": "02:00 pm - 03:15 pm (At home)",
                        "course": "Afternoon Class",
                    },
                    "time": [[14, 0], [15, 15]],
                    "position": [{3, 4}, {3, 4}, {1, 2}, {1, 2}],
                },
            ],
        },
        "courses": 2,
        "positions": {1, 2, 3, 4},
        "cycle": {
            "length": 4,
            "duration": "day",
        },
        "question": {
            "prompt": "On which day are you in person for this course?",
            "choices": [
                (1, 1),
                (2, 2),
                (3, 3),
                (4, 4),
            ],
        },
    },
    "week": {
        "schedules": {
            "default": [
                {
                    "description": {
                        "time": "09:00 am - 11:30 am",
                        "course": "Morning Class",
                    },
                    "time": [[9, 0], [11, 30]],
                    "position": [{1, 5, 7}, {3, 6, 7}],
                },
                {
                    "description": {
                        "time": "12:15 pm - 02:45 pm",
                        "course": "Afternoon Class",
                    },
                    "time": [[12, 15], [14, 45]],
                    "position": [{2, 5, 7}, {4, 6, 7}],
                },
            ],
            "late-start": [
                {
                    "description": {
                        "time": "10:00 am - 12:00 pm",
                        "course": "Morning Class",
                    },
                    "time": [[10, 0], [12, 0]],
                    "position": [{1, 5, 7}, {3, 6, 7}],
                },
                {
                    "description": {
                        "time": "12:45 pm - 02:45 pm",
                        "course": "Afternoon Class",
                    },
                    "time": [[12, 45], [14, 45]],
                    "position": [{2, 5, 7}, {4, 6, 7}],
                },
            ],
            "early-dismissal": [
                {
                    "description": {
                        "time": "09:00 am - 10:14 am",
                        "course": "Morning Class",
                    },
                    "time": [[9, 0], [10, 14]],
                    "position": [{1, 5, 7}, {3, 6, 7}],
                },
                {
                    "description": {
                        "time": "10:16 am - 11:30 am",
                        "course": "Afternoon Class",
                    },
                    "time": [[10, 16], [11, 30]],
                    "position": [{2, 5, 7}, {4, 6, 7}],
                },
            ],
            "early-early-dismissal": [
                {
                    "description": {
                        "time": "09:00 am - 9:55 am",
                        "course": "1st Classes",
                    },
                    "time": [[9, 0], [9, 55]],
                    "position": [{1, 5, 7}, {3, 6, 7}],
                },
                {
                    "description": {
                        "time": "10:00 am - 11:00 am",
                        "course": "2nd Classes",
                    },
                    "time": [[10, 0], [11, 0]],
                    "position": [{2, 5, 7}, {4, 6, 7}],
                },
            ],
        },
        "courses": 4,
        "positions": {1, 2, 3, 4, 5, 6, 7},
        "cycle": {
            "length": 2,
            "duration": "week",
        },
        "question": {
            "prompt": "When do you have class for this course?",
            "choices": [
                (1, "Week 1 Morning"),
                (2, "Week 1 Afternoon"),
                (3, "Week 2 Morning"),
                (4, "Week 2 Afternoon"),
                (5, "This course is a 2-credit Co-op in Week 1."),
                (6, "This course is a 2-credit Co-op in Week 2."),
                (7, "This course is a 4-credit Co-op."),
            ],
        },
    },
    "post-covid": {
        "schedules": {
            "default": [
                {
                    "description": {
                        "time": "09:00 am - 10:15 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 00], [10, 15]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "10:20 am - 11:35 am",
                        "course": "Period 2",
                    },
                    "time": [[10, 20], [11, 35]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "12:20 pm - 01:35 pm",
                        "course": "Period 3",
                    },
                    "time": [[12, 20], [13, 35]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "01:40 pm - 02:55 pm",
                        "course": "Period 4",
                    },
                    "time": [[13, 40], [14, 55]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "late-start": [
                {
                    "description": {
                        "time": "10:00 am - 11:00 am",
                        "course": "Period 1",
                    },
                    "time": [[10, 0], [11, 0]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "11:05 am - 12:05 am",
                        "course": "Period 2",
                    },
                    "time": [[11, 5], [12, 5]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "12:50 pm - 01:50 pm",
                        "course": "Period 3",
                    },
                    "time": [[12, 50], [13, 50]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "01:55 pm - 02:55 pm",
                        "course": "Period 4",
                    },
                    "time": [[13, 55], [14, 55]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "early-dismissal": [
                {
                    "description": {
                        "time": "09:00 am - 09:45 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 0], [9, 45]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "09:50 am - 10:30 am",
                        "course": "Period 2",
                    },
                    "time": [[9, 50], [10, 30]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "10:35 am - 11:15 am",
                        "course": "Period 3",
                    },
                    "time": [[10, 35], [11, 15]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "11:20 am - 12:00 pm",
                        "course": "Period 4",
                    },
                    "time": [[11, 20], [12, 0]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "one-hour-lunch": [
                {
                    "description": {
                        "time": "09:00 am - 10:15 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 00], [10, 15]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "10:20 am - 11:30 am",
                        "course": "Period 2",
                    },
                    "time": [[10, 20], [11, 30]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "12:30 pm - 01:40 pm",
                        "course": "Period 3",
                    },
                    "time": [[12, 30], [13, 40]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "01:45 pm - 02:55 pm",
                        "course": "Period 4",
                    },
                    "time": [[13, 45], [14, 55]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "early-early-dismissal": [
                {
                    "description": {
                        "time": "09:00 am - 09:25 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 0], [9, 25]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "09:30 am - 9:55 am",
                        "course": "Period 2",
                    },
                    "time": [[9, 30], [9, 55]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "10:00 am - 10:25 am",
                        "course": "Period 3",
                    },
                    "time": [[10, 0], [10, 25]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "10:30 am - 11:00 am",
                        "course": "Period 4",
                    },
                    "time": [[10, 30], [11, 0]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
        },
        "courses": 4,
        "positions": {1, 2, 3, 4, 5, 6},
        "cycle": {
            "length": 2,
            "duration": "day",
        },
        "question": {
            "prompt": "On Day 1, which period is this course in?",
            "choices": [
                (1, "Period 1"),
                (2, "Period 2"),
                (3, "Period 3"),
                (4, "Period 4"),
                (5, "This course is a 2-credit Co-op in the morning."),
                (6, "This course is a 2-credit Co-op in the afternoon."),
            ],
        },
    },
    "2022-2023": {
        "day_num_method": "calendar_days",
        "schedules": {
            "default": [
                {
                    "description": {
                        "time": "09:00 am - 10:20 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 0], [10, 20]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "10:25 am - 11:40 am",
                        "course": "Period 2",
                    },
                    "time": [[10, 25], [11, 40]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "12:40 pm - 01:55 pm",
                        "course": "Period 3",
                    },
                    "time": [[12, 40], [13, 55]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "02:00 pm - 03:15 pm",
                        "course": "Period 4",
                    },
                    "time": [[14, 0], [15, 15]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "late-start": [
                {
                    "description": {
                        "time": "10:00 am - 11:05 am",
                        "course": "Period 1",
                    },
                    "time": [[10, 0], [11, 5]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "11:10 am - 12:10 pm",
                        "course": "Period 2",
                    },
                    "time": [[11, 10], [12, 10]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "01:10 pm - 02:10 pm",
                        "course": "Period 3",
                    },
                    "time": [[13, 10], [14, 10]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "02:15 pm - 03:15 pm",
                        "course": "Period 4",
                    },
                    "time": [[14, 15], [15, 15]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
            "half-day": [
                {
                    "description": {
                        "time": "09:00 am - 09:45 am",
                        "course": "Period 1",
                    },
                    "time": [[9, 0], [9, 45]],
                    "position": [{1, 5}, {1, 5}],
                },
                {
                    "description": {
                        "time": "09:50 am - 10:35 pm",
                        "course": "Period 2",
                    },
                    "time": [[9, 50], [10, 35]],
                    "position": [{2, 5}, {2, 5}],
                },
                {
                    "description": {
                        "time": "10:40 pm - 11:25 pm",
                        "course": "Period 3",
                    },
                    "time": [[10, 40], [11, 25]],
                    "position": [{3, 6}, {4, 6}],
                },
                {
                    "description": {
                        "time": "11:30 pm - 12:15 pm",
                        "course": "Period 4",
                    },
                    "time": [[11, 30], [12, 15]],
                    "position": [{4, 6}, {3, 6}],
                },
            ],
        },
        "courses": 4,
        "positions": {1, 2, 3, 4, 5, 6},
        "cycle": {
            "length": 2,
            "duration": "day",
        },
        "question": {
            "prompt": "On Day 1, which period is this course in?",
            "choices": [
                (1, "Period 1"),
                (2, "Period 2"),
                (3, "Period 3"),
                (4, "Period 4"),
                (5, "This course is a 2-credit Co-op in the morning."),
                (6, "This course is a 2-credit Co-op in the afternoon."),
            ],
        },
    },
}

# Authentication settings
SESSION_SAVE_EVERY_REQUEST = True  # Refreshes session expiry  session on every request
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS
SESSION_COOKIE_AGE = 15 * 86400  # 15 days
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_FORMS = {
    "login": "allauth.account.forms.LoginForm",
    "signup": "core.forms.MetropolisSignupForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
}
LOGIN_URL = "/accounts/login"
LOGIN_REDIRECT_URL = "/accounts/profile"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ReCaptcha settings

RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
RECAPTCHA_REQUIRED_SCORE = 0.85

# NavBar settings

NAVBAR = {
    "Announcements": {
        "All": "/announcements?feed=all",
        "School": "/announcements?feed=school",
        "Student Council": "/announcements?feed=studentcouncil",
    },
    "Calendar": "/calendar",
    "Clubs": "/clubs",
    "Content": "/blog",
    "Resources": "/resources",
    "Map": "/map",
    "About": {
        "WLMCI": "/about?tab=history",
        "About": "/about?tab=about",
        "Team": "/about?tab=team",
        "Contact WLMCI": "/about?tab=school",
        "Contact Us": "/about?tab=contact",
    },
}

# Announcements settings

ANNOUNCEMENTS_CUSTOM_FEEDS = []  # list of PKs of organizations

BANNER2 = []

# Comment settings

ALLOW_COMMENTS: bool = True  # Whether to allow comments on posts

# API settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
}

# SSO (OAuth) Settings

OAUTH2_PROVIDER = dict(
    SCOPES={
        "openid": "OpenID Connect",
        "email": "Read your email address",
        "user": "Read other users' data",
        "internal": "Internal Application",
        "me_meta": "Read your account data",
        "me_announcement": "Read your announcement feed",
        "me_schedule": "Read your schedules",
        "me_timetable": "Read your timetables",
    },
    CLIENT_ID_GENERATOR_CLASS="oauth2_provider.generators.ClientIdGenerator",
    OIDC_ENABLED=True,
)

with open(os.path.join(os.path.dirname(__file__), "local_rsa_privkey.pem")) as f:
    OAUTH2_PROVIDER.update(
        dict(
            OIDC_RSA_PRIVATE_KEY=f.read(),
        )
    )

# CORS settings

CORS_URLS_REGEX = r"^/api/.*$"

CORS_ALLOW_METHODS = [
    "GET",
    "HEAD",
    "OPTIONS",
]

CORS_ALLOWED_ORIGINS = [
    "https://maclyonsden.com",
]

# Color settings

TAG_COLOR_SATURATION = 0.2
TAG_COLOR_VALUE = 1.0

# Martor settings

MARTOR_THEME = "bootstrap"
MARTOR_MARKDOWN_BASE_MENTION_URL = "/user/"
MARTOR_UPLOAD_URL = "/api/martor/upload-image"
MARTOR_UPLOAD_MEDIA_DIR = "martor"
MARTOR_UPLOAD_SAFE_EXTS = {".jpg", ".jpeg", ".png", ".gif"}
MARTOR_MARKDOWN_EXTENSIONS = [
    "markdown.extensions.tables",
    "markdown.extensions.nl2br",
    "markdown.extensions.fenced_code",
    "martor.extensions.escape_html",
    "martor.extensions.urlize",
    "core.markdown.embed",
    "core.markdown.emoji",
]

# Select2 settings

SELECT2_CACHE_BACKEND = "default"
SELECT2_JS = "js/select2.min.js"
SELECT2_CSS = "css/select2.min.css"

# PWA settings

PWA_APP_NAME = "Metropolis"
PWA_APP_DESCRIPTION = "William Lyon Mackenzie's online hub for announcements, calendar events, clubs, and timetables"
PWA_APP_THEME_COLOR = "#073763"
PWA_APP_BACKGROUND_COLOR = "#1c233f"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {
        "src": "/static/core/img/logo/logo-any-96.png",
        "sizes": "96x96",
        "type": "image/png",
        "purpose": "any",
    },
    {
        "src": "/static/core/img/logo/logo-maskable-96.png",
        "sizes": "96x96",
        "type": "image/png",
        "purpose": "maskable",
    },
    {
        "src": "/static/core/img/logo/logo-any-144.png",
        "sizes": "144x144",
        "type": "image/png",
        "purpose": "any",
    },
    {
        "src": "/static/core/img/logo/logo-maskable-144.png",
        "sizes": "144x144",
        "type": "image/png",
        "purpose": "maskable",
    },
    {
        "src": "/static/core/img/logo/logo-any-192.png",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "any",
    },
    {
        "src": "/static/core/img/logo/logo-maskable-192.png",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "maskable",
    },
]
PWA_APP_SPLASH_SCREEN = []
PWA_APP_LANG = "en-CA"
PWA_APP_DEBUG_MODE = False
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, "templates", "serviceworker.js")

# Mapbox settings

MAPBOX_APIKEY = "change me"

# Metropolis settings

METROPOLIS_STAFFS = {
    "Project Manager": {},
    "Frontend Developer": {},
    "Backend Developer": {},
    "App Developer": {},
    "Graphic Designer": {},
    "Content Creator": {},
}

METROPOLIS_STAFF_BIO = {}

# Theme Settings

THEMES = {
    "spring": {
        "banner": "/static/core/img/themes/banners/spring.jpg",
        "banner_css": "/static/core/css/themes/banners/spring-banner.css",
        "logo": "/static/core/img/themes/logos/dark-transparent.png",
        "theme": "/static/core/css/themes/base-theme.css",
    },
    "summer": {
        "banner": "/static/core/img/themes/banners/summer.jpg",
        "banner_css": "/static/core/css/themes/banners/summer-banner.css",
        "logo": "/static/core/img/themes/logos/dark-transparent.png",
        "theme": "/static/core/css/themes/base-theme.css",
    },
    "autumn": {
        "banner": "/static/core/img/themes/banners/autumn.jpg",
        "banner_css": "/static/core/css/themes/banners/autumn-banner.css",
        "logo": "/static/core/img/themes/logos/dark-transparent.png",
        "theme": "/static/core/css/themes/base-theme.css",
    },
    "winter": {
        "banner": "/static/core/img/themes/banners/winter.jpg",
        "banner_css": "/static/core/css/themes/banners/winter-banner.css",
        "logo": "/static/core/img/themes/logos/dark-transparent.png",
        "theme": "/static/core/css/themes/base-theme.css",
    },
    "valentines": {
        "banner": "/static/core/img/themes/banners/valentines.jpg",
        "banner_css": "/static/core/css/themes/banners/valentines-banner.css",
        "logo": "/static/core/img/themes/logos/valentines-transparent.png",
        "theme": "/static/core/css/themes/valentines-theme.css",
    },
    "halloween": {
        "banner": "/static/core/img/themes/banners/halloween.jpg",
        "banner_css": "/static/core/css/themes/banners/halloween-banner.css",
        "logo": "/static/core/img/themes/logos/halloween-transparent.png",
        "theme": "/static/core/css/themes/halloween-theme.css",
    },
    "remembrance": {
        "banner": "/static/core/img/themes/banners/winter.jpg",
        "banner_css": "/static/core/css/themes/banners/winter-banner.css",
        "logo": "/static/core/img/themes/logos/remembrance-transparent.png",
        "theme": "/static/core/css/themes/base-theme.css",
    },
    "christmas": {
        "banner": "/static/core/img/themes/banners/christmas.jpg",
        "banner_css": "/static/core/css/themes/banners/christmas-banner.css",
        "logo": "/static/core/img/themes/logos/christmas-transparent.png",
        "theme": "/static/core/css/themes/christmas-theme.css",
    },
    "39": {
        "banner": "/static/core/img/themes/banners/spring.jpg",
        "banner_css": "/static/core/css/themes/banners/spring-banner.css",
        "logo": "/static/core/img/themes/logos/dark-transparent.png",
        "theme": "/static/core/css/themes/39-theme.css",
    },
}

CURRENT_THEME = "spring"

# Lazy Loading

LAZY_LOADING = {  # set to False to disable
    "per_page": 1,
    "initial_limit": 1,
}

# Misc settings

SITE_ID = 1

SITE_URL = "http://127.0.0.1:8000"

TOS_URL = "/terms/"
PRIVPOL_URL = "/privacy/"

CRISPY_TEMPLATE_PACK = "bootstrap4"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SILENCED_SYSTEM_CHECKS = ["urls.W002"]

API_VERSION = "3.2.0"

DEFAULT_TIMEZONE = "UTC"

ANNOUNCEMENT_APPROVAL_BCC_LIST = []

ROOT = "http://localhost"

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "UPDATE_LAST_LOGIN": True,
}
# Event calender Settings


ICAL_PADDING = timedelta(days=4 * 7)  # iCalendar Feed
REOCCURRENCE_CUTOFF = timedelta(
    days=365 * 2
)  # For reoccurring events only calculate up to x years in advance

# Qualified Trials
QLTR: Dict[str, Dict] = {
    "ann-draft": dict(
        title="Announcement Status Default as Draft",
    ),
    "ia": dict(
        title="Cumulative Minor Changes to Index",
    ),
}

THEME_BANNER = THEMES[CURRENT_THEME]["banner"]
THEME_BANNER_CSS = THEMES[CURRENT_THEME]["banner_css"]
THEME_LOGO = THEMES[CURRENT_THEME]["logo"]
THEME_CSS = THEMES[CURRENT_THEME]["theme"]

TEACHER_EMAIL_SUFFIX = "@tdsb.on.ca"
STUDENT_EMAIL_SUFFIX = "@student.tdsb.on.ca"

PRE = ""

BANNER3: List = [
    dict(
        start=timezone.now(),
        end=timezone.now() + timedelta(days=1),
        content="This is some banner :)",
        icon_url="non-blank means default (default only now)",
        cta_link="https://nyiyui.ca",
        cta_label="some shameless plug to nowhere amirite",
    ),
]

CELERY_TIMEZONE = "America/Toronto"

# (Expo) Notifications

NOTIF_EXPO_TIMEOUT_SECS = 3

ANNOUNCEMENTS_NOTIFY_FEEDS = []  # list of PKs of organizations
EVENTS_NOTIFY_FEEDS = []  # list of PKs of organizations
NOTIF_DRY_RUN = True

try:
    from metropolis.config import *
except ImportError as err:
    pass
else:
    import warnings

    warnings.warn(DeprecationWarning("use local_settings.py instead of config.py"))

try:
    with open(os.path.join(os.path.dirname(__file__), "local_settings.py")) as f:
        exec(f.read(), globals())
except IOError:
    pass

if SECRET_KEY == "Change me":
    raise TypeError("override SECRET_KEY")


def is_aware(d: datetime) -> bool:
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None


def check_banner3(banner: Dict) -> None:
    assert is_aware(banner["start"])
    assert is_aware(banner["end"])
    assert bool(banner.get("cta_link")) == bool(banner.get("cta_label"))


for banner in BANNER3:
    check_banner3(banner)


def compat_conv(banner: Dict) -> Dict:
    banner2 = {}
    banner2["logo"] = "icon_url" in banner
    banner2["text"] = banner["content"]
    banner2["show_btn"] = "cta_link" in banner
    banner2["url"] = banner.get("cta_link")
    banner2["url_text"] = banner.get("cta_label")
    return banner2


now = timezone.now()
BANNER2 += list(
    map(compat_conv, filter(lambda b: b["start"] < now < b["end"], BANNER3))
)
