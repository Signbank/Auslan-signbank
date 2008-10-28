from django import forms
from django.contrib.formtools.preview import FormPreview 
from auslan.video.fields import VideoUploadToFLVField


class GlossUpdateForm(forms.Form):
    """Form for updating selective elements of a gloss"""
     
    # fields used from the main update page
    inWeb = forms.BooleanField(required=False)
    inMedLex = forms.BooleanField(required=False)
    keyword = forms.CharField(max_length=50, widget=forms.HiddenInput, required=False)
    n = forms.IntegerField(widget=forms.HiddenInput, required=False)
  
  
    
class VideoUpdateForm(forms.Form):
    """Form to allow update of the video for a sign"""    
    videofile = VideoUploadToFLVField()  
    

