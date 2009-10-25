from django.conf.urls.defaults import *
from django.conf import settings
import registration.forms

from django.views.generic.simple import direct_to_template


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^$', 'auslan.views.index'),
    
    (r'^(?P<flavour>dictionary|medical)/', include('auslan.dictionary.urls')),
    (r'^feedback/', include('auslan.feedback.urls')),
    (r'^attachments/', include('auslan.attachments.urls')),

    (r'^register.html', 'auslan.views.index'), 
    (r'^logout.html', 'django.contrib.auth.views.logout',
                       {'next_page': "/"}),
    
    
    (r'^spell/twohanded.html$', direct_to_template, {'template': 'fingerspell/fingerspellingtwohanded.html'}),
    (r'^spell/onehanded.html$', direct_to_template, {'template': 'fingerspell/fingerspellingonehanded.html'}),
    (r'^numbersigns.html$', direct_to_template, {'template': 'numbersigns/numbersigns.html'}),

 
    
    # compatibility with old links - intercept and return 401
    (r'^index.cfm', direct_to_template, {'template': 'compat.html',}),

   # (r'^accounts/login/', 'django.contrib.auth.views.login'),
        
    (r'^accounts/', include('auslan.registration.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    (r'^admin/(.*)', admin.site.root),


    (r'^test.html$', 'django.views.generic.simple.direct_to_template', {'template': 'test.html'}),    
)


# location for static media
# this should be removed in a production system
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', 
             {'document_root': 'media'}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
        (r'^video/comments/(?P<path>.*)$', 'django.views.static.serve', 
             {'document_root': settings.COMMENT_VIDEO_LOCATION}),
  
    )
   
    

