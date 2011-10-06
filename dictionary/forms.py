from django import forms
from django.contrib.formtools.preview import FormPreview 
from signbank.video.fields import VideoUploadToFLVField
from signbank.dictionary.models import Dialect, Gloss
from django.conf import settings

class GlossModelForm(forms.ModelForm):
    class Meta:
        model = Gloss
        # fields are defined in settings.py
        fields = settings.QUICK_UPDATE_GLOSS_FIELDS
  
    
class VideoUpdateForm(forms.Form):
    """Form to allow update of the video for a sign"""    
    videofile = VideoUploadToFLVField()  
    

