"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os, random, string
from pathlib import Path
from dotenv import load_dotenv

# Import for CORS headers
from corsheaders.defaults import default_headers
from django.contrib.messages import constants as messages
load_dotenv()  # take environment variables from .env.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

# Render Deployment Code
#DEBUG = False
#original: 
# DEBUG = 'RENDER' not in os.environ
PRODUCTION = 'RUN_MAIN' not in os.environ
# Set DEBUG based on the environment. TO test 404 locally, set Debug = False.
DEBUG = not PRODUCTION


# Docker HOST
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Add here your deployment HOSTS
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:5085']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:    
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

#Secure Cookies
#Ensure cookies are only sent over HTTPS
SESSION_COOKIE_SECURE = True

# Prevents JavaScript from accessing session cookies
SESSION_COOKIE_HTTPONLY = True

#Mitigate CSRF attacks by restricting cross-origin cookie sharing
SESSION_COOKIE_SAMESITE = 'Strict'

#Ensure CSRF cookies are sent over HTTPS only
CSRF_COOKIE_SECURE = True

#Enhance CSRF protection
CSRF_COOKIE_SAMESITE = 'Strict'

#Ensure DEBUG is set to False in production to avoid sensitive information exposure
DEBUG = True


#Limit request header sizes and body lenghts
#Limit number of form fileds
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000 

# Limit max upload memory size 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  



# Application definition

INSTALLED_APPS = [
   'crispy_forms',
    'tinymce',
    'crispy_bootstrap5',
    "django_light",
    # "django.contrib.admin",
    "core.apps.CustomAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",


 
    'rest_framework',  
    'drf_yasg', 

    'home',
    'theme_pixel',
    'corsheaders',

]

MIDDLEWARE = [
    # CORS middleware must come before commonmiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'xss_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'xss_attempts.log',
        },
    },
    'loggers': {
        'xss_logger': {
            'handlers': ['xss_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

ROOT_URLCONF = "core.urls"

HOME_TEMPLATES = os.path.join(BASE_DIR, 'home', 'templates')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
DB_USERNAME = os.getenv('DB_USERNAME' , None)
DB_PASS     = os.getenv('DB_PASS'     , None)
DB_HOST     = os.getenv('DB_HOST'     , None)
DB_PORT     = os.getenv('DB_PORT'     , None)
DB_NAME     = os.getenv('DB_NAME'     , None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = { 
      'default': {
        'ENGINE'  : 'django.db.backends.' + DB_ENGINE, 
        'NAME'    : DB_NAME,
        'USER'    : DB_USERNAME,
        'PASSWORD': DB_PASS,
        'HOST'    : DB_HOST,
        'PORT'    : DB_PORT,
        }, 
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = "home.User"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

# TIME_ZONE = "UTC"
TIME_ZONE = "Australia/Melbourne"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'custom_static/'
# STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'custom_static')
]


#if not DEBUG:
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587 # For TLS, 465 for SSL
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hardhatcompanywebsite@gmail.com'
EMAIL_HOST_PASSWORD = 'nuje nbmo cfqe skjb'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

MESSAGE_TAGS = {
    messages.ERROR: 'error'
}

#EMAIL_HOST_USER = {'kaviuln@gmail.com'}

MESSAGE_TAGS = {
    messages.SUCCESS: 'success'
}


# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Protect against clickjacking
X_FRAME_OPTIONS = 'DENY'  # Use 'SAMEORIGIN' if the site needs to be embedded in iframes from the same origin

# Enable XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Enforce HTTPS (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


 
 
# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',  # Website localhost server url
    'https://hardhatwebdev2024.pythonanywhere.com',    # Frontend url
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies or other credentials

CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-type',
    'authorization',
]

