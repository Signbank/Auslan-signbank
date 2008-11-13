from django.conf.urls.defaults import *

urlpatterns = patterns('auslan.pages.views',
    (r'^(?P<url>.*)$', 'page'),
)
