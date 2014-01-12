from django.conf.urls.defaults import *
from signbank.dictionary.models import *
from signbank.dictionary.forms import *

from signbank.dictionary.adminviews import GlossListView, GlossDetailView


urlpatterns = patterns('',

    # index page is just the search page
    (r'^$', 'signbank.dictionary.views.index'),

    # we use the same view for a definition and for the feedback form on that
    # definition, the first component of the path is word or feedback in each case
    (r'^words/(?P<keyword>.+)-(?P<n>\d+).html$',
            'signbank.dictionary.views.word'),

    url(r'^tag/(?P<tag>[^/]*)/?$', 'signbank.dictionary.tagviews.taglist'),

    # and and alternate view for direct display of a gloss
    (r'gloss/(?P<idgloss>.+).html$', 'signbank.dictionary.views.gloss'),

    url(r'^search/$', 'signbank.dictionary.views.search', name="dictionary-search"),
    (r'^update/gloss/(?P<glossid>\d+)$', 'signbank.dictionary.update.update_gloss'),
    (r'^update/tag/(?P<glossid>\d+)$', 'signbank.dictionary.update.add_tag'),
    (r'^update/video/(?P<glossid>\d+)$', 'signbank.dictionary.update.update_video'),

    (r'^ajax/keyword/(?P<prefix>.*)$', 'signbank.dictionary.views.keyword_value_list'),

    (r'^missingvideo.html$', 'signbank.dictionary.views.missing_video_view'),

    url(r'^export.csv', 'signbank.dictionary.views.csv_export', name='export'),

    # Admin views
    url(r'^list/$', GlossListView.as_view(), name='admin_gloss_list'),
    url(r'^gloss/(?P<pk>\d+)', GlossDetailView.as_view(), name='admin_gloss_view'),

)


