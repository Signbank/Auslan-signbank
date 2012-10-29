from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import Context, RequestContext
from models import Video, GlossVideo
from forms import VideoUploadForm, VideoUploadForGlossForm
from convertvideo import extract_frame

def addvideo(request): 
    """View to present a video upload form and process
    the upload"""
       
    if request.method == 'POST':
        
        form = VideoUploadForGlossForm(request.POST, request.FILES)
        if form.is_valid():
            sn = form.cleaned_data['gloss_sn']
            vfile = form.cleaned_data['videofile']
            vfile.name = sn+".mp4"
            redirect_url = form.cleaned_data['redirect']
                        
            # deal with any existing video for this sign
            oldvids = GlossVideo.objects.filter(gloss_sn=sn)
            for v in oldvids:
                v.reversion()

            video = GlossVideo(videofile=vfile, gloss_sn=sn)
            video.save()
            
            
            # TODO: provide some feedback that it worked (if
            # immediate display of video isn't working)
            return redirect(redirect_url)
    
    # if we can't process the form, just redirect back to the 
    # referring page, should just be the case of hitting
    # Upload without choosing a file but could be 
    # a malicious request, if no referrer, go back to root
    if request.META.has_key('HTTP_REFERER'):
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)


def deletevideo(request, videoid):
    """Remove the video for this gloss, if there is an older version
    then reinstate that as the current video (act like undo)"""
    
    if request.method == "POST":
        # deal with any existing video for this sign
        vids = GlossVideo.objects.filter(gloss_sn=videoid)
        for v in vids:
            # this will remove the most recent video, ie it's equivalent
            # to delete if version=0
            v.reversion(revert=True)
            
    # TODO: provide some feedback that it worked (if
    # immediate non-display of video isn't working)
    
    # return to referer
    if request.META.has_key('HTTP_REFERER'):
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)

    
def poster(request, videoid):
    """Generate a still frame for a video (if needed) and 
    generate a redirect to the static server for this frame"""
    
    video = get_object_or_404(GlossVideo, gloss_sn=videoid)
    
    return redirect(video.poster_url())


def video(request, videoid):
    """Redirect to the video url for this videoid"""
    
    video = get_object_or_404(GlossVideo, gloss_sn=videoid)
    
    return redirect(video)
    
def iframe(request, videoid):
    """Generate an iframe with a player for this video"""
    
    video = get_object_or_404(GlossVideo, gloss_sn=videoid, version=0)
    
    return render_to_response("iframe.html",
                              {'videourl': video.get_absolute_url(),
                               'posterurl': video.poster_url(),
                               })
    
    
    
