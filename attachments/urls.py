from django.conf.urls.defaults import *
from auslan.attachments.models import *

urlpatterns = patterns('',
    
    (r'^$', 'django.views.generic.list_detail.object_list',
       {'queryset': Attachment.objects.all(),
        'template_name': 'list.html',
       }),
    (r'^upload/', 'auslan.attachments.views.upload_file'),
)

