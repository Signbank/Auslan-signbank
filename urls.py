from django.conf.urls.defaults import *
from django.conf import settings
import registration.forms

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^$', 'auslan.views.index'),
    
    (r'^(?P<flavour>dictionary|medical)/', include('auslan.dictionary.urls')),
    (r'^feedback/', include('auslan.feedback.urls')),

    (r'^fingerspellingtwohanded.html', 'auslan.views.fingerspellingtwohanded'),
    (r'^fingerspellingonehanded.html', 'auslan.views.fingerspellingonehanded'),
    
    
    (r'^numbersigns/', 'auslan.views.numbersigns'),
    # because of the flowplayer problem we redirect numbersigns to a 
    # static version of the page on the media server
    (r'^numbersigns.html', 'django.views.generic.simple.redirect_to', 
                           {'url': settings.AUSLAN_STATIC_PREFIX+"pages/numbersigns.html" }),

    (r'^register.html', 'auslan.views.register'), 
    (r'^logout.html', 'django.contrib.auth.views.logout',
                       {'template_name': "index.html"}),
    
    # compatibility with old links - intercept and return 401
    (r'^index.cfm', 'django.views.generic.simple.direct_to_template', {'template': 'compat.html',}),
                       
   # (r'^accounts/login/', 'django.contrib.auth.views.login'),
        
    (r'^accounts/', include('auslan.registration.urls')),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    (r'^admin/(.*)', admin.site.root),
    
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
   
    

