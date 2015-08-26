from django.conf.urls import *
from django.conf import settings
import registration.forms
from django.conf.urls.static import static
from django.views.generic import TemplateView

from signbank.dictionary.models import Gloss

from django.contrib import admin
admin.autodiscover()

from adminsite import publisher_admin

if settings.SHOW_NUMBERSIGNS:
    numbersigns_view = TemplateView.as_view(template_name='numbersigns/numbersigns.html')
else:
    numbersigns_view = TemplateView.as_view(template_name='numbersigns/underconstruction.html')


urlpatterns = patterns('',

    url(r'^$', 'signbank.pages.views.page', name='root_page'),

    url(r'^dictionary/', include('signbank.dictionary.urls', namespace='dictionary')),
    url(r'^feedback/', include('signbank.feedback.urls')),
    url(r'^attachments/', include('signbank.attachments.urls')),
    url(r'^video/', include('signbank.video.urls')),

    #(r'^register.html', 'signbank.views.index'),
    url(r'^logout.html', 'django.contrib.auth.views.logout',
                       {'next_page': "/"}, "logout"),


    url(r'^spell/twohanded.html$', TemplateView.as_view(template_name='fingerspell/fingerspellingtwohanded.html')),
    url(r'^spell/practice.html$', TemplateView.as_view(template_name='fingerspell/fingerspellingpractice.html')),
    url(r'^spell/onehanded.html$', TemplateView.as_view(template_name='fingerspell/fingerspellingonehanded.html')),
    url(r'^numbersigns.html$', numbersigns_view),

    # compatibility with old links - intercept and return 401
    url(r'^index.cfm', TemplateView.as_view(template_name='compat.html')),

   # (r'^accounts/login/', 'django.contrib.auth.views.login'),

    url(r'^accounts/', include('signbank.registration.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # special admin sub site
    url(r'^publisher/', include(publisher_admin.urls)),
    
    
    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^test/(?P<videofile>.*)$', TemplateView.as_view(template_name="test.html")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





