
import logging
import sys
from django.conf import settings

def init_logging():
    logging.basicConfig(filename=settings.LOG_FILENAME, level=logging.DEBUG)

def debug(msg):
    logging.debug(msg)

logInitDone=False
if not logInitDone:
    logInitDone = True
    init_logging()
