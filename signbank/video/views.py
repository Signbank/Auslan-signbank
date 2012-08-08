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
            video = GlossVideo(videofile=vfile, gloss_sn=sn)
            video.save()
    else:
        form = VideoUploadForGlossForm()
        video = None
        
    return render_to_response("addvideo.html",
                              {'form': form,
                              'video': video,
                              'error': None
                              }, context_instance=RequestContext(request) )

def add_video_for_gloss(request): 
    """View to present a video upload form for adding a new video to a gloss"""
       
    if request.method == 'POST':
        
        form = VideoUploadForGlossForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save() 
    else:
        form = VideoUploadForm()
        video = None
        
    return render_to_response("addvideo.html",
                              {'form': form,
                              'video': video,
                              'error': None
                              }, context_instance=RequestContext(request) )
    
    

    
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
    
    video = get_object_or_404(GlossVideo, gloss_sn=videoid)
    
    return render_to_response("iframe.html",
                              {'videourl': video.get_absolute_url(),
                               'posterurl': video.poster_url(),
                               })
    
    
    
