from settings_base import *

import os.path

import mongobean.orm as orm
orm.default_db = orm.pymongo.MongoClient().sozialfunk_development


EMAIL_ACTION_REPEAT_TIME = 20
EMAIL_INFO_FROM_ADDRESS = 'Sozialfunk <noreply@sozialfunk.de>'
EMAIL_USE_HTML = False
IGNORE_MISSING_BETA_KEY = True
CONFIRM_SIGNUP_BY_ADMIN = True

DEVELOPMENT = False

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sozialfunk_production',                      # Or path to database file if using sqlite3.
        'USER': 'sozialfunk',                      # Not used with sqlite3.
        'PASSWORD': 'sozialfunk',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
