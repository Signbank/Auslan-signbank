# Django settings for auslan project.

ADMINS = (
     ('Steve Cassidy', 'steve.cassidy@mq.edu.au'),
)

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = "webmaster@auslan.org.au"

TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-us'

# site_id
#   1 = www.auslan.org.au
#   2 = beta.auslan.org.au
SITE_ID = 1
USE_I18N = True

# URL for login, used by automatic redirects to login 
# for views marked with the login required decorator
LOGIN_URL = '/accounts/login/'

## Settings for the registration module
ACCOUNT_ACTIVATION_DAYS = 2

# do we show the registration form or not
ALLOW_REGISTRATION = True

## User session cookies should expire on closing the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'svyc8#was2(t$(fw=a&f8i+1o7n(pgubh=le*j-tg-0uwmaxl3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader', 
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'middleware.UserBasedExceptionMiddleware',
    'signbank.pages.middleware.PageFallbackMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "signbank.pages.context_processors.menu",
    "django_mobile.context_processors.flavour", 
)


TEMPLATE_TAGS = ('signbank.dictionary.templatetags.prefixes', )

# add the Email backend to allow logins using email as username
AUTHENTICATION_BACKENDS = (
    "signbank.registration.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin', 
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'signbank.dictionary',
    'signbank.feedback',
    'signbank.registration',
    'signbank.pages',
    'signbank.attachments',
    'signbank.video',
    'south',
    'reversion',
    'django_mobile',
    'tagging',
)

ROOT_URLCONF = 'signbank.urls'
LOGIN_REDIRECT_URL = '/feedback/'



# these settings might be over-ridden by settings_local.py 
DEBUG = True
TEMPLATE_DEBUG = DEBUG
EMAIL_HOST = "mail.exetel.com.au" 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'signbank.db',                 
    }
}

# Absolute path to the directory that holds media. 
MEDIA_ROOT = 'test-media'
# URL that handles the media served from MEDIA_ROOT. 
MEDIA_URL = '/media/'

# Ditto for static files from the Auslan site (css, etc) with trailing slash 
AUSLAN_STATIC_PREFIX = "/static/"

# Django 1.4 provides support for static files, should port the above to this...
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = ''

# URL prefix for static files. 
STATIC_URL = '/statics/'

# List of finder classes that know how to find static files in
# various locations.
#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
#)





# location of ffmpeg, used to convert uploaded videos
FFMPEG_PROGRAM = "/Applications/ffmpegX.app/Contents/Resources/ffmpeg"
FFMPEG_TIMEOUT = 60
FFMPEG_OPTIONS = ["-vcodec", "h264", "-an"]

TEMPLATE_DIRS = (
    'templates'
)

# turn on lots of logging or not
DO_LOGGING = False
LOG_FILENAME = "debug.log"

# location and URL for uploaded files
UPLOAD_ROOT = MEDIA_ROOT + "upload/" 
UPLOAD_URL = MEDIA_URL + "upload/"

# Location for comment videos relative to MEDIA_ROOT
COMMENT_VIDEO_LOCATION = "comments"
# Location for videos associated with pages
PAGES_VIDEO_LOCATION = 'pages'
# location for upload of videos relative to MEDIA_ROOT
# videos are stored here prior to copying over to the main
# storage location
VIDEO_UPLOAD_LOCATION = "upload"

# within MEDIA_ROOT we look for videos in these directories, trying them in order
# and only looking further down the list if the required video isn't found
# new video uploads are only put in the first of these 
VIDEO_DIRECTORIES = ["bsl-video", "video"]

# which fields from the Gloss model should be included in the quick update form on the sign view
QUICK_UPDATE_GLOSS_FIELDS = ['language', 'dialect']

# should we always require a login for viewing dictionary content
ALWAYS_REQUIRE_LOGIN = False

# name of the primary css file, one of 'auslan', 'bsl' or 'test-server'
PRIMARY_CSS = "test-server"

# settings for django-mobile

# settings for django-tagging

FORCE_LOWERCASE_TAGS = True

# import local settings if present
try:
    from settings_local import *
except:
    pass





## settings that depend on things that might be over-ridden





