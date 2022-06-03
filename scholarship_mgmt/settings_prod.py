"""
Django settings for scholarship_mgmt project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""


import os
import stripe
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gchy7$_ctk45##d%(p*+*v6ciju3&#h72dwfz2ugx%u11q1)c&'
#HASHING_SECRET_KEY = 'ctk45##d%(p*+*v6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'accounts.apps.AccountsConfig',
    'common.apps.CommonConfig',
    'masters.apps.MastersConfig',
    'student.apps.StudentConfig',
    'partner.apps.PartnerConfig',
    'accounting.apps.AccountingConfig',
    'donor.apps.DonorConfig',
    'parent.apps.ParentConfig',
    'mathfilters',
    'password_reset.apps.PasswordResetConfig',
    'payments.apps.PaymentsConfig',
    'rest_api',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

}

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

ROOT_URLCONF = 'scholarship_mgmt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'accounts.views.get_user_permission',
            ],
        },
    },
]


WSGI_APPLICATION = 'scholarship_mgmt.wsgi.application'

AUTH_USER_MODEL = "accounts.User"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'


FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}



DATABASES = {
     'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'uni_sys_production_db',
          # 'NAME': 'indonesia_university_system_test_v2',
          'USER':'riyaz',
          'PASSWORD':'Sayyed@123',
          'HOST': '127.0.0.1',
          'PORT':'3306'
     }
 }




'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sayyedriyaj55@gmail.com'
EMAIL_HOST_PASSWORD = 'Sayyed@123'
EMAIL_USE_TLS = True


# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
#
#
# EMAIL_HOST_USER = 'namafund@namafoundation.org'
# EMAIL_HOST_PASSWORD = 'namafund123'
# EMAIL_PORT = 587
SERVER_HOST_NAME = "http://34.83.191.75/"

stripe.api_key = 'sk_test_51JcmDhSIeVZrpBOQmSMJtfkhTDY8JkkrbnjdEw2wurzt9nQdK74CGYCX90l5q0VfEUuq4oLzQHMA1mgpeUqsKK6G00fUXuYOIG'

STRIPE_SECRET_KEY = 'sk_test_51JcmDhSIeVZrpBOQmSMJtfkhTDY8JkkrbnjdEw2wurzt9nQdK74CGYCX90l5q0VfEUuq4oLzQHMA1mgpeUqsKK6G00fUXuYOIG'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51JcmDhSIeVZrpBOQvbNkpUdU9H7l6iGwMyHzsASeNF6howwGwp9asyxWfjukiP7bHqB5EnGKIwGBR02f5431Qni700Zf86Q6VI'



USE_I18N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', _('English')),
    ('id', _('Indonesian')),
)