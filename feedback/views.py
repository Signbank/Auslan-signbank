
import os
from models import *
from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, HttpResponseRedirect

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
    
    general = GeneralFeedback.objects.filter(status='unread')
    missing = MissingSignFeedback.objects.filter(status='unread')
    signfb = SignFeedback.objects.filter(status__in=('unread', 'read'))
    
    return render_to_response("feedback/show.html",
                              {'general': general,    
                              'missing': missing,
                              'signfb': signfb,
                              }, 
                              context_instance=RequestContext(request))
    
    
    
    
# Feedback on individual signs
@login_required
def signfeedback(request, keyword, n):
    """View or give feedback on a sign"""
    
    n = int(n)
    word = get_object_or_404(Keyword, text=keyword)
    
    # returns (matching translation, number of matches) 
    (trans, total) =  word.match_request(request, n)
    
    # get the page to return to from the get request
    if request.GET.has_key('return'):
        sourcepage = request.GET['return']
    else:
        sourcepage = ""
    
    valid = False
    
    if request.method == "POST":
        feedback_form = SignFeedbackForm(request.POST)
        
        if feedback_form.is_valid():
            # get the clean (normalised) data from the feedback_form
            clean = feedback_form.cleaned_data
            # create a SignFeedback object to store the result in the db
            sfb = SignFeedback(
                isAuslan=clean['isAuslan'],
                whereused=clean['whereused'],
                like=clean['like'],
                use=clean['use'],
                suggested=clean['suggested'],
                correct=clean['correct'],
                kwnotbelong=clean['kwnotbelong'],
                comment=clean['comment'],
                user=request.user,
                translation_id = request.POST["translation_id"]
                )
            sfb.save()
            valid = True
            # redirect to the original page
            return HttpResponseRedirect(sourcepage+"?feedbackmessage='Thank you. Your feedback has been saved.")
    else:
        feedback_form = SignFeedbackForm()
        
    return render_to_response("feedback/signfeedback.html",
                              {'translation': trans,
                               'n': n, 
                               'total': total,   
                               'feedback_form': feedback_form, 
                               'valid': valid,
                               'sourcepage': sourcepage
                               },
                               context_instance=RequestContext(request))


#--------------------
#  deleting feedback
#--------------------

def delete(request, kind, id):
    """Mark a feedback item as deleted, kind 'signfeedback', 'generalfeedback' or 'missingsign'"""
    
    if kind == 'sign':
        kind = SignFeedback
    elif kind == 'general':
        kind = GeneralFeedback
    elif kind == 'missingsign':
        kind = MissingSignFeedback
    else:
        raise Http404
    
    item = get_object_or_404(kind, id=id)
    # mark as deleted
    item.status = 'deleted'
    item.save()
    return HttpResponse("deleted "+str(item), content_type='text/plain')


