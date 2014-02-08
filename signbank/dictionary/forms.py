from django import forms
from django.contrib.formtools.preview import FormPreview
from signbank.video.fields import VideoUploadToFLVField
from signbank.dictionary.models import Dialect, Gloss
from django.conf import settings
from tagging.models import Tag

class GlossModelForm(forms.ModelForm):
    class Meta:
        model = Gloss
        # fields are defined in settings.py
        fields = settings.QUICK_UPDATE_GLOSS_FIELDS


class VideoUpdateForm(forms.Form):
    """Form to allow update of the video for a sign"""
    videofile = VideoUploadToFLVField()


class TagUpdateForm(forms.Form):
    """Form to add a new tag to a gloss"""

    tag = forms.ModelChoiceField(queryset=Tag.objects.all())
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput)
    
    
class GlossSearchForm(forms.ModelForm):
    
    search = forms.CharField(label="Search Gloss/SN")
    tags = forms.CharField(label="Tagged")
    nottags = forms.CharField(label="Not Tagged")
    keyword = forms.CharField(label='Keyword')
    
    class Meta:
        model = Gloss
        fields = ('idgloss', 'annotation_idgloss', 'morph', 'sense', 
                   'sn', 'StemSN', 'comptf', 'compound', 'language', 'dialect',
                   'inWeb', 'isNew',
                   'initial_relative_orientation', 'final_relative_orientation',
                   'initial_palm_orientation', 'final_palm_orientation', 
                   'initial_secondary_loc', 'final_secondary_loc',
                   'domhndsh', 'subhndsh', 'locprim', 'locsecond',
                   'final_domhndsh', 'final_subhndsh', 'final_loc'
                   )
    


