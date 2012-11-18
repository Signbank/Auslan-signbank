"""Convert a video file to flv"""

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError  
from signbank.video.convertvideo import convert_video

import os

class Command(BaseCommand):
     
    help = 'convert a video file to some format'
    args = 'source dest'

    def handle(self, *args, **options):
        
        if len(args) == 2:
            source = args[0] 
            dest = args[1]
            
            convert_video_collection(source, dest)
     
        else:
            print "Usage convertvideo", self.args
            
            
            

def convert_video_collection(sourcedir, destdir):
    """Convert all video files in this collection"""
    
    for dir in os.listdir(sourcedir):
        if os.path.isdir(os.path.join(sourcedir, dir)):
            if not os.path.exists(os.path.join(destdir, dir)):
                os.makedirs(os.path.join(destdir, dir))

            for f in os.listdir(os.path.join(sourcedir, dir)):
                (name, ext) = os.path.splitext(f)
                if ext in ['.mp4', '.flv']:
                    sourcefile = os.path.join(sourcedir, dir, f)
                    destfile = os.path.join(destdir, dir, name+".mp4")
                    if not os.path.exists(destfile):
                        print sourcefile, destfile  
                        convert_video(sourcefile, destfile, force=True)
                    





