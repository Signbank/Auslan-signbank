from django.conf.urls.defaults import *
from auslan.dictionary.models import *

urlpatterns = patterns('',
    
    (r'^$', 'auslan.feedback.views.index'),
    
    (r'^show.html', 'auslan.feedback.views.showfeedback'),
    (r'^missingsign.html', 'auslan.feedback.views.missingsign'), 
    (r'^generalfeedback.html', 'auslan.feedback.views.generalfeedback'),
    
    (r'^sign/(?P<keyword>.+)-(?P<n>\d+).html$',  'auslan.feedback.views.signfeedback'),
   
   
    (r'^(?P<kind>general|sign|missingsign)/delete/(?P<id>\d+)$', 'auslan.feedback.views.delete'),
)


