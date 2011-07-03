from django import forms
from django.contrib.formtools.preview import FormPreview 
from signbank.video.fields import VideoUploadToFLVField
from signbank.dictionary.models import Dialect, Gloss


class GlossUpdateForm(forms.Form):
    """Form for updating selective elements of a gloss"""
     
    # fields used from the main update page
    inWeb = forms.BooleanField(label="Include in the web dictionary?", required=False)
    inMedLex = forms.BooleanField(label="Problematic Medical Sign?", required=False)
    healthtf = forms.BooleanField(label="Medical Sign?", required=False)
    keyword = forms.CharField(max_length=50, widget=forms.HiddenInput, required=False)
    n = forms.IntegerField(widget=forms.HiddenInput, required=False)
    dialect = forms.ModelMultipleChoiceField(label="Dialect", queryset=Dialect.objects.all(), required=False)#, widget=forms.CheckboxSelectMultiple)

class GlossModelForm(forms.ModelForm):
    class Meta:
        model = Gloss
        fields = ['inWeb', 'InMedLex', 'healthtf', 'language', 'dialect']
  
    
class VideoUpdateForm(forms.Form):
    """Form to allow update of the video for a sign"""    
    videofile = VideoUploadToFLVField()  
    

