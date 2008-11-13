
from django.core.files.uploadedfile import UploadedFile
from django.forms.util import ValidationError
from django import forms
from django.conf import settings
import sys, os, time, signal
from subprocess import Popen, PIPE
from tempfile import mkstemp

class UploadedFLVFile(UploadedFile):
    """
    A file converted to FLV.
    """
    def __init__(self, name):  
        self.name = name  
        self.field_name = None
        self.content_type = 'video/flv'
        self.charset = None
        self.file = open(name)
    
    def read(self, *args):          return self.file.read(*args)
    def seek(self, *args):          return self.file.seek(*args)
    def tell(self, *args):          return self.file.tell(*args)
    def __iter__(self):             return iter(self.file)
    def readlines(self, size=None): return self.file.readlines(size)
    def xreadlines(self):           return self.file.xreadlines()

    
    def rename(self, location):
        """Rename (move) the file to a new location on disk"""

        os.rename(self.name, location)
        self.name = location
        
    def delete(self):
        """Remove the file"""
        os.unlink(self.name)
        

class VideoUploadToFLVField(forms.FileField):
    """A custom form field that supports uploading video
    files and converting them to FLV (flash video) before 
    saving"""

    def __init__(self, geometry="300x240", prefix='upload', **kwargs):
        """
        Added fields:
            - geometry: specify the geometry of the final video, eg. "300x240"
            
        """

        super(VideoUploadToFLVField, self).__init__(**kwargs)
        self.geometry = geometry
        self.prefix = prefix


    def clean(self, data, initial=None):
        """Checks that the file is valid video and converts it to
        FLV format"""
        
        f = super(VideoUploadToFLVField, self).clean(data, initial)
        if f is None:
            return None
        elif not data and initial:
            return initial

        # We need the data to be in a real file for ffmpeg. 
        # either it's already written out to a tmp file or
        # we have to do it here
        
        if hasattr(data, 'temporary_file_path'):
            tmpname = data.temporary_file_path()
        else:
            # need to store in-memory data out to a temp file
            if settings.FILE_UPLOAD_TEMP_DIR:
                (tmp, tmpname) = mkstemp(prefix=self.prefix, 
                                         dir=settings.FILE_UPLOAD_TEMP_DIR)
            else:
                (tmp, tmpname) = mkstemp(prefix=self.prefix)

            
            for chunk in f.chunks():
                os.write(tmp,chunk)
            os.close(tmp)
            
        # construct an flv filename
        flvfile = tmpname+".flv"
        # now do the conversion to flv
        if self.convert_to_flv(tmpname, flvfile):
            # we want to return an UploadedFile obj representing
            # the flv file, not the original but I can't 
            # create one of those from an existing file
            # so I use my own wrapper class            
            print "Converted to flash: ", flvfile

            os.unlink(tmpname)
            return UploadedFLVFile(flvfile)
        else:
            raise ValidationError("Conversion of video failed: please try to use a diffent format")
        
        


    def convert_to_flv(self, sourcefile, targetfile):
        """Convert video to flv format"""
                
        ffmpeg = [settings.FFMPEG_PROGRAM, "-y", "-v", "-1", "-i", sourcefile, "-f", "flv", "-s", self.geometry, targetfile]
     
        process =  Popen(ffmpeg, stdout=PIPE, stderr=PIPE)
        start = time.time()
        
        while process.poll() == None: 
            if time.time()-start > settings.FFMPEG_TIMEOUT:
                # we've gone over time, kill the process  
                os.kill(process.pid, signal.SIGKILL)
                raise ValidationError("Conversion of video took too long. Please try another format.")
        

        status = process.poll()
        #out,err = process.communicate()

        # Check if file exists and is > 0 Bytes
        try:
            s = os.stat(targetfile) 
            fsize = s.st_size
            if (fsize == 0):
                os.remove(targetfile)
                return False
            else:
                return True
        except:
            return False


