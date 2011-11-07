"""Convert a video file to flv"""

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError  
from signbank.video.convertvideo import convert_video


class Command(BaseCommand):
     
    help = 'convert a video file to some format'
    args = 'infile outfile'

    def handle(self, *args, **options):
        
        if len(args) == 2:
            infile = args[0] 
            outfile = args[1]
            
            convert_video(infile, outfile)
     
        else:
            print "Usage convertvideo", self.args