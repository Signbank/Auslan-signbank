""" Models for the video application
keep track of uploaded videos and converted versions
"""
 
from django.db import models
from django.conf import settings
import sys, os, time

from convertvideo import extract_frame, convert_video

from django.core.files.storage import FileSystemStorage


class VideoPosterMixin:
    """Base class for video models that adds a method
    for generating poster images
    
    Concrete class should have fields 'videofile' and 'poster'
    """

    def poster_path(self, create=True):
        """Return the path of the poster image for this
        video, if create=True, create the image if needed
        Return None if create=False and the file doesn't exist"""
        
        vidpath, ext = os.path.splitext(self.videofile.path)
        poster_path = vidpath + ".jpg"
        
        if not os.path.exists(poster_path):
            # need to create the image
            extract_frame(self.videofile.path, poster_path)
        
        return poster_path

    def poster_url(self):
        """Return the URL of the poster image for this video"""
        
        # generate the poster image if needed
        path = self.poster_path()
        
        # splitext works on urls too!
        vidurl, ext = os.path.splitext(self.videofile.url)
        poster_url = vidurl + ".jpg"
        
        return poster_url
    
    def get_absolute_url(self):
        
        return self.videofile.url
    
    def ensure_mp4(self):
        """Ensure that the video file is an h264 format
        video, convert it if necessary"""
        
        pass
    

    def delete_files(self):
        """Delete the files associated with this object"""
        
        try:
            os.unlink(self.videofile.path)
            poster_path = self.poster_path(create=False)
            if poster_path:
                os.unlink(poster_path)
        except:
            pass


class Video(models.Model, VideoPosterMixin):
    """A video file stored on the site"""
    
    # video file name relative to MEDIA_ROOT
    videofile = models.FileField("Video file in h264 mp4 format", upload_to=settings.VIDEO_UPLOAD_LOCATION)
    
    def __unicode__(self):
        return self.videofile.name
    

import shutil

class GlossVideoStorage(FileSystemStorage):
    """Implement our shadowing video storage system"""
    
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(GlossVideoStorage, self).__init__(location, base_url)
        self.directories = settings.VIDEO_DIRECTORIES
    
    
    def get_valid_name(self, name):
    
        (targetdir, basename) = os.path.split(name)
        
        path = os.path.join(str(basename)[:2], str(basename))
        
        # new files always go in the first of our directories
        dirname = self.directories[0]
                
        result = os.path.join(targetdir, dirname, path)
        print "Valid name: ", result
        return result
        
    def get_available_name(self, name):
        """Return an available file name, map the name to
        a subdirectory named for the first two characters of the
        name"""
     
        fullpath = os.path.join(settings.MEDIA_ROOT, name)
        # check that this file doesn't already exist
        if os.path.exists(fullpath):
            # if it does...we make a backup of the current file
            # and allow the new file to take this name
            shutil.move(fullpath, fullpath+".bak")
            
        print "available name", name
        return name

    
    
    
storage = GlossVideoStorage(location=settings.MEDIA_ROOT)

class GlossVideo(models.Model, VideoPosterMixin):
    """A video that represents a particular idgloss"""
    
    videofile = models.FileField("video file", upload_to='.', storage=storage)
    gloss_sn = models.CharField("Gloss SN", max_length=20)
    
    def __unicode__(self):
        return self.videofile.name
    
    


    