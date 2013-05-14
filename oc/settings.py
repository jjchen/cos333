# Django settings for oc project.

DEBUG = False
TEMPLATE_DEBUG = False

# Public: www.cos333-oc.herokuapp.com/
#FACEBOOK_APP_ID = '431733443585073'
#FACEBOOK_API_SECRET = 'bee41bd237e61feb159d64f99e7db996'

# Private: localhost:8000
FACEBOOK_APP_ID =  '125667410957888'
FACEBOOK_API_SECRET = '1d71ff77879df12aa55ba2307523ab04'

FACEBOOK_EXTENDED_PERMISSIONS = ['user_events', 'friends_events',
                                 'create_event', 'rsvp_event', 'user_groups',
                                 'read_friendlists']

LOGIN_URL = '/frontend/login/facebook'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/error/'

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_USER_MODEL = 'frontend.MyUser'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3mruqbl01mt9e',
        # The following settings are not used with sqlite3:
        'USER': 'gvvmlwjnckcrtz',
        'PASSWORD': '8S9bKm59d8esQj7BYH1PbE9VP5',
        'HOST': 'ec2-54-225-69-193.compute-1.amazonaws.com',                  
        'PORT': '5432',                    
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = '*'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TAGGING_AUTOCOMPLETE_MAX_TAGS = 5

TAGGING_AUTOCOMPLETE_JQUERY_UI_FILE = 'http://code.jquery.com/ui/1.10.2/jquery-ui.js'

TAGGING_AUTOCOMPLETE_CSS = (
    'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/jquery-ui-1.9.2.custom.css',
    'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/jquery.ui.1.10.0.ie.css',
    'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/jquery-ui-1.10.0.custom.css',
    #'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/jquery.tagit.css',
    #'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/tagit.ui-zendesk.css',
    #'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/ui-autocomplete-tag-it.css',
    'TAGGING_AUTOCOMPLETE_JS_BASE_URL/css/jquery.ui.1.9.2.ie.css',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u3x7_a7=+a^mong!uz!m4!$1gx)%j1um*=#@%+6b+$d4!gn*ro'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_cas.middleware.CASMiddleware',
    'django.middleware.doc.XViewMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CAS_SERVER_URL = 'https://fed.princeton.edu/cas/'
CAS_REDIRECT_URL = '/frontend/'
ROOT_URLCONF = 'oc.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'oc.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
	'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'polls',
    'timeline',
    'frontend',
    'social_auth',
    #'tagging',
    #'tagging_autocomplete_tagit',
    'south'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django_cas.backends.CASBackend',
    'django.contrib.auth.backends.ModelBackend'
)

