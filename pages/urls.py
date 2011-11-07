from django.conf.urls.defaults import *

urlpatterns = patterns('signbank.pages.views',
    (r'^(?P<url>.*)$', 'page'),
)
