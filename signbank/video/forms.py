from django import forms
from models import Video, GlossVideo

class VideoUploadForm(forms.ModelForm):
    """Form for video upload"""
    
    class Meta:
        model = GlossVideo
        
class VideoUploadForGlossForm(forms.Form):
    """Form for video upload for a particular gloss"""
    
    videofile = forms.FileField()
    gloss_sn = forms.CharField()
    