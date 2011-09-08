from django.conf.urls.defaults import *
from signbank.attachments.models import *

urlpatterns = patterns('',
    
    (r'^$', 'django.views.generic.list_detail.object_list',
       {'queryset': Attachment.objects.all(),
        'template_name': 'list.html',
       }, "attachments"),
    (r'^upload/', 'signbank.attachments.views.upload_file'),
)

