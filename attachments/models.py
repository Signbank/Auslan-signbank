from django.db import models
from django.contrib.auth import models as authmodels
from django.conf import settings

# Models for file attachments uploaded to the site
# basically just a simple container for files
# but allowing for replacement of previously uploaded files

class Attachment(models.Model):
    
    file = models.FileField(upload_to='/media')
    description = models.TextField(blank=True)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(authmodels.User)
    
    