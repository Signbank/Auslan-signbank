from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django import forms
import os.path
from django.core.files import File
from auslan.attachments.models import Attachment

# TODO: both list and upload views should be handled by the same view fn
# TODO: deal with uploading duplicate files - offer to replace 

class UploadFileForm(forms.Form): 
    file  = forms.FileField()
    description = forms.CharField()

def handle_uploaded_file(request, fileobj):
    """Store the uploaded file"""
     
    fullpath = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_ROOT, "attachments", fileobj.name)
    relname = os.path.join(settings.UPLOAD_ROOT, "attachments", fileobj.name)
    if not os.path.exists(os.path.dirname(fullpath)):
        os.makedirs(os.path.dirname(fullpath))
    
    destination = open(fullpath, 'wb+')
    for chunk in fileobj.chunks():
       destination.write(chunk)
    destination.close()

    # create and save a new attachment object
    a = Attachment(file=relname, description=request.POST['description'], uploader=request.user)
    a.save()
    
    return relname

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            destname = handle_uploaded_file(request, request.FILES['file']) 
            return HttpResponseRedirect('/attachments/')
    return HttpResponseRedirect('/attachments/')
        

