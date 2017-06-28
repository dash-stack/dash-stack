"""
Django settings for palamar project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@b*)c#tfs%382t87hojq!1pou#f_3557kf(w@a++y$j5)+$rmd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'palamar',
    '127.0.0.1',
    'localhost',
    'demo.palamar.io'
]

# fullt qualified hostname or domain. Ex <http://domain.tld/>
SITE_ROOT_URL = 'http://127.0.0.1:8000'

# login url
LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/'

# logout redirect
LOGOUT_REDIRECT_URL = '/auth/login/'


# user profile
AUTH_PROFILE_MODULE = 'user_profile.Profile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cuser',
    'app',
    'authcp',
    'admincp',
    'container',
    'domain',
    'image',
    'network',
    'security',
    'sites',
    'user_profile',
    'project',
    'role',
    'quota',
    'social_django',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'cuser.middleware.CuserMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'palamar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'libraries': {
                'custom_tags': 'templatetags.custom_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'palamar.wsgi.application'

# logging configuration

if DEBUG == True:
    LOG_LEVEL = 'DEBUG'
else:
    LOG_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': '/var/log/palamar/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'palamar',
        'USER': 'palamar',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

#static url
STATIC_URL = '/static/'

# media location
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# file location
FILE_STORAGE = os.path.join(BASE_DIR, "files")


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'mail.host'

# Port for sending e-mail.
EMAIL_PORT = 587

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_EMAIL_FROM = 'admin@palamar.org'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'authcp.views.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

# Google auth settings

# SECURITY WARNING: keep the secret key used in production secret!
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '58128956219-lobtqsd956c9cpqvsd5ml2hvaa35ps9o'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'RNXY2W32PhAsGVZKx8WsxTmK'


# Facebook auth settings
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.9'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}

SOCIAL_AUTH_FACEBOOK_KEY = '1816310968617086'
# SECURITY WARNING: keep the secret key used in production secret!
SOCIAL_AUTH_FACEBOOK_SECRET = '413880eed823c86f6e519afe0ae19341'


# GITHUB auth settings

SOCIAL_AUTH_GITHUB_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_PROFILE_EXTRA_PARAMS = {
    'fields': 'name,email',
}

SOCIAL_AUTH_GITHUB_KEY = '07d27678fffaa29bc2cc'
# SECURITY WARNING: keep the secret key used in production secret!
SOCIAL_AUTH_GITHUB_SECRET = '23991546f87c828ed1e5699a48641c3b99daeae9'

# split settings
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass