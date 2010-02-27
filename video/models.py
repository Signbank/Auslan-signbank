""" Models for the video application
keep track of uploaded videos and converted versions
"""
 
from django.db import models
from django.conf import settings
from django.http import Http404
from subprocess import Popen, PIPE

import sys, os, time


class Video(models.Model):
    """An uploaded video that will be converted to a form suitable for
    web delivery and then associated with either a sign or a comment on the site"""

    geometry = models.CharField("Target geometry for converted files", max_length="20", default="320x240")
    
    original = models.FileField("Original uploaded file", upload_to=settings.MEDIA_ROOT)
    h264 = models.FileField("h264 (mp4) version of file", upload_to=settings.MEDIA_ROOT)
    ogg = models.FileField("ogg theora version of file", upload_to=settings.MEDIA_ROOT)
    
    
    
def ffmpeg(sourcefile, format, geometry, targetfile):
    """Convert video to some new format via ffmpeg
    
    Raises ValidationError if there is some problem with file
    conversion.
    
    If conversion works, just exits quietly, targetfile should
    be the newly converted file.
    
    """

    errormsg = ""
    
    # ffmpeg command options:
    #  -y  answer yes to all queries
    #  -v -1 be less verbose
    # -i sourcefile   input file
    # -f <format> output format
    # -an no audio in output
    # -s <geometry> set size of output
    # 
    ffmpeg = [settings.FFMPEG_PROGRAM, "-y", "-v", "-1", "-i", sourcefile, "-f", format, "-an", "-s", geometry, targetfile]
 
    #debug(ffmpeg)
    
    process =  Popen(ffmpeg, stdout=PIPE, stderr=PIPE)
    start = time.time()
    
    while process.poll() == None: 
        if time.time()-start > settings.FFMPEG_TIMEOUT:
            # we've gone over time, kill the process  
            os.kill(process.pid, signal.SIGKILL)
            debug("Killing ffmpeg process")
            errormsg = "Conversion of video took too long.  This site is only able to host relatively short videos."
    

    status = process.poll()
    #out,err = process.communicate()

    # Check if file exists and is > 0 Bytes
    try:
        s = os.stat(targetfile) 
        fsize = s.st_size
        if (fsize == 0):
            os.remove(targetfile)
            errormsg = "Conversion of video failed: please try to use a diffent format"
    except:
        errormsg = "Conversion of video failed: please try to use a different video format"
        
    if errormsg:
        # we have a conversion error
        # notify the admins, attaching the offending file
        msgtxt = "Error: %s\n\nCommand: %s\n\n" % (errormsg, " ".join(ffmpeg))
        
        message = EmailMessage("Video conversion failed on Auslan",
                               msgtxt,
                               to=[a[1] for a in settings.ADMINS])
        message.attach_file(sourcefile)
        message.send(fail_silently=False)
        
        
        # and raise a validation error for the caller
        raise ValidationError(errormsg)
