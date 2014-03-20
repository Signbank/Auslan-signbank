from django.conf.urls import *

urlpatterns = patterns('',
    
    (r'^video/(?P<videoid>.*)$', 'signbank.video.views.video'),
    (r'^upload/', 'signbank.video.views.addvideo'),
    (r'^delete/(?P<videoid>.*)$', 'signbank.video.views.deletevideo'),
    (r'^poster/(?P<videoid>.*)$', 'signbank.video.views.poster'),
    (r'^iframe/(?P<videoid>.*)$', 'signbank.video.views.iframe'),
)


