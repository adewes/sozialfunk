from settings_base import *
from secret_settings_development import *

import os.path

import mongobean.orm as orm
orm.default_db = orm.pymongo.MongoClient().sozialfunk_development


DEVELOPMENT = True

DEBUG = True
TEMPLATE_DEBUG = True

import djcelery

"""
Settings for Celery.
"""
djcelery.setup_loader()

BROKER_URL = "amqp://sozialfunk:sozialfunk@localhost:5672/sozialfunk"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tweets.tasks", )
CELERYD=PROJECT_PATH+"/../manage.py celeryd"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sozialfunk_development',                      # Or path to database file if using sqlite3.
        'USER': 'sozialfunk',                      # Not used with sqlite3.
        'PASSWORD': 'sozialfunk',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
