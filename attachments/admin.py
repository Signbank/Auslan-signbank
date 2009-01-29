from django.contrib import admin 
from auslan.attachments.models import *
 
class AttachmentAdmin(admin.ModelAdmin):
   list_display = ['file', 'date', 'uploader']
   
admin.site.register(Attachment, AttachmentAdmin)
