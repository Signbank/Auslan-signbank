from django.conf.urls.defaults import *
from django.conf import settings
import registration.forms

from django.views.generic.simple import direct_to_template
from signbank.dictionary.models import Gloss

from tagging.views import tagged_object_list

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^$', 'signbank.pages.views.page', name='root_page'),
    
    url(r'^(?P<version>dictionary|medical)/', include('signbank.dictionary.urls')),
    url(r'^feedback/', include('signbank.feedback.urls')),
    url(r'^attachments/', include('signbank.attachments.urls')),

    #(r'^register.html', 'signbank.views.index'), 
    url(r'^logout.html', 'django.contrib.auth.views.logout',
                       {'next_page': "/"}, "logout"),
    
    
    url(r'^spell/twohanded.html$', direct_to_template, {'template': 'fingerspell/fingerspellingtwohanded.html'}),
    url(r'^spell/practice.html$', direct_to_template, {'template': 'fingerspell/fingerspellingpractice.html'}),
    url(r'^spell/onehanded.html$', direct_to_template, {'template': 'fingerspell/fingerspellingonehanded.html'}),
    url(r'^numbersigns.html$', direct_to_template, {'template': 'numbersigns/numbersigns.html'}),

 
    
    # compatibility with old links - intercept and return 401
    url(r'^index.cfm', direct_to_template, {'template': 'compat.html',}),

   # (r'^accounts/login/', 'django.contrib.auth.views.login'),
        
    url(r'^accounts/', include('signbank.registration.urls')),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),  
    url(r'^admin/', include(admin.site.urls)), 

    url(r'^test/(?P<videofile>.*)$', 'django.views.generic.simple.direct_to_template', {'template': 'test.html'}),    
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
   
    

