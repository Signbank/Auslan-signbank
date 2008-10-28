
import os
from models import *
from django import forms
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

import time

def index(request):
    return render_to_response('feedback/index.html',
                              { 'menuid':5, 'submenuid':1, 'title':"Leave Feedback"},
                              context_instance=RequestContext(request))

        

@login_required
def generalfeedback(request):
    feedback = GeneralFeedback()
    valid = False
   
    if request.method == "POST":
        form = GeneralFeedbackForm(request.POST, request.FILES)
        if form.is_valid():           
            
            feedback = GeneralFeedback(user=request.user)
            if form.cleaned_data.has_key('comment'): 
                feedback.comment = form.cleaned_data['comment'] 
            
            if form.cleaned_data.has_key('video') and form.cleaned_data['video'] != None:
                video = form.cleaned_data['video']
                # copy to comment video location
                basename = os.path.split(video.name)[-1]
                # make sure the target directory is there
                targetdir = os.path.join(settings.MEDIA_ROOT, settings.COMMENT_VIDEO_LOCATION)
                if not os.path.exists(targetdir):
                    os.mkdir(targetdir)
                commentloc = os.path.join(targetdir, basename)
                video.rename(commentloc)
                
                feedback.video = os.path.join(settings.COMMENT_VIDEO_LOCATION, basename)
            feedback.save()
            valid = True
    else:
        form = GeneralFeedbackForm()

    return render_to_response("feedback/generalfeedback.html",
                              {'menuid':5, 
                               'submenuid':3, 
                               'title':"General Feedback",
                               'form': form,
                               'valid': valid },
                               context_instance=RequestContext(request)
                              )

@login_required
def missingsign(request):

    posted = False # was the feedback posted?
    
    if request.method == "POST":
        
        fb = MissingSignFeedback()
        fb.user = request.user
        
        form = MissingSignFeedbackForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            
            # either we get video of the new sign or we get the 
            # description via the form
            
            if form.cleaned_data.has_key('video') and form.cleaned_data['video'] != None:
                video = form.cleaned_data['video']
                # copy to comment video location
                basename = os.path.split(video.name)[-1]
                # make sure the target directory is there
                targetdir = os.path.join(settings.MEDIA_ROOT, settings.COMMENT_VIDEO_LOCATION)
                if not os.path.exists(targetdir):
                    os.mkdir(targetdir)
                commentloc = os.path.join(targetdir, basename)
                video.rename(commentloc)
                # put the video pathname to the feedback object
                fb.video = os.path.join(settings.COMMENT_VIDEO_LOCATION, basename)
            else:
                # get sign details from the form 
                fb.handform = form.cleaned_data['handform'] 
                fb.handshape = form.cleaned_data['handshape']
                fb.althandshape = form.cleaned_data['althandshape']
                fb.location = form.cleaned_data['location']
                fb.relativelocation = form.cleaned_data['relativelocation']
                fb.handbodycontact = form.cleaned_data['handbodycontact']
                fb.handinteraction = form.cleaned_data['handinteraction']
                fb.direction = form.cleaned_data['direction']
                fb.movementtype = form.cleaned_data['movementtype']
                fb.smallmovement = form.cleaned_data['smallmovement']
                fb.repetition = form.cleaned_data['repetition']
            
            # these last two are required either way (video or not)
            fb.meaning = form.cleaned_data['meaning']
            fb.comments = form.cleaned_data['comments']
    
            fb.save()
            posted = True
    else:
        form = MissingSignFeedbackForm()        
  
    
    return render_to_response('feedback/missingsign.html',
                               {'menuid':5, 
                                'submenuid':2, 
                                'title':"Report a Missing Sign",
                                'posted': posted,
                                'form': form
                                },
                              context_instance=RequestContext(request))

                              
#-----------
# views to show feedback to Trevor et al
#-----------

@login_required
def showfeedback(request):
    """View to list the feedback that's been left on the site"""
    
    general = GeneralFeedback.objects.all()
    missing = MissingSignFeedback.objects.all()
    signfb = SignFeedback.objects.all()
    
    return render_to_response("feedback/show.html",
                              {'general': general,    
                              'missing': missing,
                              'signfb': signfb,
                              }, 
                              context_instance=RequestContext(request))
    
