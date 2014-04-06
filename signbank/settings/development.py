from signbank.settings.base import *


TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'bootstrap_templates'),
)

PRIMARY_CSS = "bootstrap_css/bsl.css"

# what do we call this signbank?
SIGNBANK_NAME = "BSL"

# show/don't show sign navigation
SIGN_NAVIGATION = False

# show the number signs page or an under construction page?
SHOW_NUMBERSIGNS = False

# which definition fields do we show and in what order?
#DEFINITION_FIELDS = []

ADMIN_RESULT_FIELDS = ['idgloss', 'annotation_idgloss']


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


import mimetypes
mimetypes.add_type("video/mp4", ".mov", True)
    
    
    