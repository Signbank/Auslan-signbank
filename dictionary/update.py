from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings 
from django.contrib.auth.decorators import permission_required


import os

from auslan.dictionary.models import *
from auslan.dictionary.forms import * 
 
def update_gloss(request, glossid, flavour='dictionary'):
    """View to update a gloss from the form displayed on the staff view"""
    
    if not request.user.has_perm('dictionary.change_gloss'):
        return HttpResponseForbidden("Gloss Update Not Allowed")    
    
    thisgloss = None
    confirm_form = None 
    if request.method == "POST":
        update_form = GlossUpdateForm(request.POST, request.FILES)
        if update_form.is_valid():
            clean = update_form.cleaned_data
            thisgloss = get_object_or_404(Gloss, id=glossid)
            
            # inWeb is only present if it's selected hence:
            if clean.has_key('inWeb'):
                thisgloss.inWeb = clean['inWeb']
            else:
                thisgloss.inWeb = False
                
            if clean.has_key('inMedLex'):
                thisgloss.InMedLex = clean['inMedLex']
            else:
                thisgloss.InMedLex = False
                
            thisgloss.save()
        
        referer = request.META['HTTP_REFERER']
        
        return render_to_response("dictionary/update_result.html", 
                              {'update_form': update_form,
                               'confirm_form': confirm_form,
                               'gloss' : thisgloss,
                               'referer': referer, 
                               },
                              context_instance=RequestContext(request))

def update_video(request, glossid, flavour='dictionary'):
    """View to update the video for a gloss from the form displayed on the staff view"""
    
    if not request.user.has_perm('dictionary.update_video'):
        return HttpResponseForbidden("Video Upload Not Allowed")
        
        
    keyword = None
    n = None 
    videofile = None
    status = "form"
    
    thisgloss = get_object_or_404(Gloss, id=glossid)

    if request.method == "POST":
        form = VideoUpdateForm(request.POST, request.FILES)
        if form.is_valid(): 
            if form.cleaned_data.has_key('videofile'):
                video = form.cleaned_data['videofile']
                # copy to comment video location
                basename = os.path.split(video.name)[-1]
                # this will be the path to the video, relative to MEDIA_ROOT
                videofile = os.path.join(settings.VIDEO_UPLOAD_LOCATION, basename)
                # make sure the target directory is there
                targetdir = os.path.join(settings.MEDIA_ROOT, settings.VIDEO_UPLOAD_LOCATION)
                if not os.path.exists(targetdir):
                    os.mkdir(targetdir)
                    
                videoloc = os.path.join(settings.MEDIA_ROOT, videofile)
                video.rename(videoloc)
                
        elif request.POST.has_key("confirmvideofile"):
            # we're in the second stage confirmation
            videofile = request.POST['confirmvideofile']
            fullpath = os.path.join(settings.MEDIA_ROOT, videofile)
            
            if request.POST.has_key("Cancel"):
                if request.POST['Cancel'] == "cancel":
                    # remove the pending video file
                    if os.access(fullpath, os.F_OK):
                        os.unlink(fullpath)
                    status = "cancelled"
            else: 
                # copy video to proper location
                newlocation = os.path.join(settings.MEDIA_ROOT, thisgloss.get_video_url())
                # backup existing file if any, create a hard link
                if os.access(newlocation, os.F_OK):
                    backup = newlocation + ".bak"
                    if os.access(backup, os.F_OK):
                        os.unlink(backup)
                    os.link(newlocation, backup)
                 
                os.rename(fullpath, newlocation)
                status = "completed"
    else: 
        form = VideoUpdateForm()

    return render_to_response("dictionary/update_video.html", 
                              {'form': form, 
                               'gloss' : thisgloss,
                               'keyword': keyword, 
                               'n': n,
                               'videofile': videofile, 
                               'status': status,
                               },
                              context_instance=RequestContext(request))
 
    
