from django.conf.urls.defaults import *
from auslan.dictionary.models import *
from auslan.dictionary.forms import *


urlpatterns = patterns('',
    
    # index page is just the search page
    (r'^$', 'auslan.dictionary.views.index'),

    # we use the same view for a definition and for the feedback form on that
    # definition, the first component of the path is word or feedback in each case
    (r'^(?P<viewname>(words|feedback))/(?P<keyword>.+)-(?P<n>\d+).html$', 
            'auslan.dictionary.views.word'),
    
    (r'^viewfeedback/(?P<keyword>.+)-(?P<n>\d+).html$', 
            'auslan.dictionary.views.viewfeedback'),
            
    # and and alternate view for direct display of a gloss
    (r'gloss/(?P<idgloss>.+).html$', 'auslan.dictionary.views.gloss'),
   
    (r'^search/$', 'auslan.dictionary.views.search'),
    (r'^update/gloss/(?P<glossid>\d+)$', 'auslan.dictionary.update.update_gloss'),
    (r'^update/video/(?P<glossid>\d+)$', 'auslan.dictionary.update.update_video'),
    
    (r'^ajax/keyword/(?P<prefix>.*)$', 'auslan.dictionary.views.keyword_value_list'),      

)


