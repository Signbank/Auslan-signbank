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
SITE_ID = 2
USE_I18N = True

# URL for login, used by automatic redirects to login 
# for views marked with the login required decorator
LOGIN_URL = '/accounts/login/'

## Settings for the registration module
ACCOUNT_ACTIVATION_DAYS = 2

## User session cookies should expire on closing the browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'svyc8#was2(t$(fw=a&f8i+1o7n(pgubh=le*j-tg-0uwmaxl3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source', 
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'auslan.middleware.UserBasedExceptionMiddleware',
    'auslan.pages.middleware.PageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "auslan.pages.context_processors.menu",
 
    )
 


TEMPLATE_TAGS = ('auslan.dictionary.templatetags.prefixes', )

# add the Email backend to allow logins using email as username
AUTHENTICATION_BACKENDS = (
    "auslan.registration.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin', 
    'django.contrib.admindocs',
    'auslan.dictionary',
    'auslan.feedback',
    'auslan.registration',
    'auslan.pages',
    'auslan.attachments',
)

ROOT_URLCONF = 'auslan.urls'
LOGIN_REDIRECT_URL = '/feedback/'

## server specific settings

# look at the hostname to see if we're on the production server
import socket
production = (socket.gethostname() == 'stevecassidy.net')

if production:
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    EMAIL_HOST =  "localhost"
    
    DATABASE_ENGINE = 'mysql'          
    DATABASE_NAME = 'auslan'          
    DATABASE_USER = 'auslan'            
    DATABASE_PASSWORD = 'trevorC5A'        
    DATABASE_HOST = ''             
    DATABASE_PORT = '' 
    
    # Absolute path to the directory that holds media. 
    MEDIA_ROOT = '/var/www-auslan-media/'
    # URL that handles the media served from MEDIA_ROOT. 
    MEDIA_URL = '/media/'
    
    # URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
    # trailing slash.
    ADMIN_MEDIA_PREFIX = '/djangomedia/'
    
    # Ditto for static files from the Auslan site (css, etc) with trailing slash 
    AUSLAN_STATIC_PREFIX = "/media/media-beta/"
    
    # location of ffmpeg, used to convert uploaded videos
    FFMPEG_PROGRAM = "/usr/bin/ffmpeg"
    FFMPEG_TIMEOUT = 60
    
    TEMPLATE_DIRS = (
        '/var/django/auslan/templates'
    )
    
    LOG_FILENAME = "/var/log/auslan-debug.log"
    
    
else:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    EMAIL_HOST = "mail.optusnet.com.au" 
    
    DATABASE_ENGINE = 'sqlite3'          
    DATABASE_NAME = 'auslan.db'          
    DATABASE_USER = ''            
    DATABASE_PASSWORD = ''        
    DATABASE_HOST = ''             
    DATABASE_PORT = '' 
    
    # Absolute path to the directory that holds media. 
    MEDIA_ROOT = '/Users/steve/projects/auslan-newlayout/auslan/media/'
    # URL that handles the media served from MEDIA_ROOT. 
    MEDIA_URL = '/media/'
    
    ADMIN_MEDIA_PREFIX = "/adminmedia/"
    
    # Ditto for static files from the Auslan site (css, etc) with trailing slash 
    AUSLAN_STATIC_PREFIX = "/static/"
 
    # location of ffmpeg, used to convert uploaded videos
    FFMPEG_PROGRAM = "/Applications/ffmpegX.app/Contents/Resources/ffmpeg"
    FFMPEG_TIMEOUT = 60
    
    TEMPLATE_DIRS = (
        'templates'
    )

    EMAIL_HOST = 'smtp.ics.mq.edu.au'
    
    LOG_FILENAME = "debug.log"



# location and URL for uploaded files
UPLOAD_ROOT = MEDIA_ROOT + "upload/" 
UPLOAD_URL = MEDIA_URL + "upload/"



# Location for comment videos relative to MEDIA_ROOT
COMMENT_VIDEO_LOCATION = "comments/"
# Location for videos associated with pages
PAGES_VIDEO_LOCATION = 'pages/'
# location for upload of videos relative to MEDIA_ROOT
# videos are stored here prior to copying over to the main
# storage location
VIDEO_UPLOAD_LOCATION = "upload/"


