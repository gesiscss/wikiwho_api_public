from .settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['local_host', '127.0.0.1']
INTERNAL_IPS = ['127.0.0.1']

# Pickle folder paths without ending /
# PICKLE_FOLDER = 'tmp_pickles'
PICKLE_FOLDER_EN = 'tmp_pickles/en'
PICKLE_FOLDER_EU = 'tmp_pickles/eu'

INSTALLED_APPS += ['debug_toolbar',
                   'debug_panel']

MIDDLEWARE_CLASSES += ['debug_panel.middleware.DebugPanelMiddleware']

SWAGGER_SETTINGS['VALIDATOR_URL'] = 'https://online.swagger.io/validator'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }

# Default logging for Django. This sends an email to the site admins on every
# HTTP 500 error. Depending on DEBUG, all other log records are either sent to
# the console (DEBUG=True) or discarded (DEBUG=False) by means of the
# require_debug_true filter.
# https://docs.djangoproject.com/en/1.10/topics/logging/#examples
