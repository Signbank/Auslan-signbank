from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from models import *

def addvideo(request): 
    """View to present a video upload form and process
    the upload"""
       
    
    if request.method == 'POST':
        
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            videofile = form.cleaned_data['videofile']
            role = form.cleaned_data['role']
            print "VIDEO: ", videofile.name, role
            # could now copy this video to somewhere else
            #videofile.rename("/tmp/uploaded.flv")
            # we should at least delete the file before exiting the view
            videofile.delete()
    else:
        form = VideoUploadForm()
        
    return render_to_response("addvideo.html",
                              {'form': form,
                              'flvfile': None,
                              'error': None
                              }, context_instance=RequestContext(request) )
    
    
