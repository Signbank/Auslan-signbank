from signbank.settings.base import *


TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'bootstrap_templates'),
)

PRIMARY_CSS = "bootstrap_css/bsl.css"

# what do we call this signbank?
SIGNBANK_NAME = "BSL"

# show/don't show sign navigation
SIGN_NAVIGATION = False

# which definition fields do we show and in what order?
#DEFINITION_FIELDS = []

GLOSS_VIDEO_DIRECTORY = 'glossvideo'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}