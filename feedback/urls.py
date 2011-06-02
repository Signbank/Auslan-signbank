from django.conf.urls.defaults import *
from signbank.dictionary.models import *

urlpatterns = patterns('',
    
    (r'^$', 'signbank.feedback.views.index'),
    
    (r'^show.html', 'signbank.feedback.views.showfeedback'),
    (r'^missingsign.html', 'signbank.feedback.views.missingsign'), 
    (r'^generalfeedback.html', 'signbank.feedback.views.generalfeedback'),
    
    (r'^sign/(?P<keyword>.+)-(?P<n>\d+).html$',  'signbank.feedback.views.signfeedback'),
   
    (r'^gloss/(?P<glossid>.+).html$',  'signbank.feedback.views.glossfeedback'),
   
   
    (r'^(?P<kind>general|sign|missingsign)/delete/(?P<id>\d+)$', 'signbank.feedback.views.delete'),
)


