from signbank.settings.base import *

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'bootstrap_templates'),
)



# what do we call this signbank?
SIGNBANK_NAME = "BSL"

# don't show sign navigation
SIGN_NAVIGATION = False

# which definition fields do we show and in what order?
#DEFINITION_FIELDS = []