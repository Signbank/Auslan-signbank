"""Convert a video file to flv"""

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError  
from auslan.video.models import ffmpeg


class Command(BaseCommand):
     
    help = 'convert a video file to some format'
    args = 'infile format geometry outfile'

    def handle(self, *args, **options):
        
        if len(args) == 4:
            infile = args[0]
            format = args[1]
            geometry = args[2]
            outfile = args[3]
                 
            ffmpeg(infile, format, geometry, outfile)
        else:
            print "Usage ..."