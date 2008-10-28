from django.conf.urls.defaults import *
from auslan.dictionary.models import *

urlpatterns = patterns('',
    
    (r'^$', 'auslan.feedback.views.index'),
    
    (r'^show.html', 'auslan.feedback.views.showfeedback'),
    (r'^missingsign.html', 'auslan.feedback.views.missingsign'), 
    (r'^generalfeedback.html', 'auslan.feedback.views.generalfeedback'),  
   
)


