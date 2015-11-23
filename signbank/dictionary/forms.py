from django import forms
from django.contrib.formtools.preview import FormPreview
from signbank.video.fields import VideoUploadToFLVField
from signbank.dictionary.models import Dialect, Gloss, Definition, Relation, Region, defn_role_choices,\
    Relationrole
from django.conf import settings
from tagging.models import Tag

# category choices are tag values that we'll restrict search to
CATEGORY_CHOICES = (('all', 'All Signs'),
                    ('semantic:health', 'Only Health Related Signs'),
                    ('semantic:education', 'Only Education Related Signs'))

class UserSignSearchForm(forms.Form):

    query = forms.CharField(label='Keywords starting with', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(label='Search', choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        

class GlossModelForm(forms.ModelForm):
    class Meta:
        model = Gloss
        # fields are defined in settings.py
        fields = settings.QUICK_UPDATE_GLOSS_FIELDS

class GlossCreateForm(forms.ModelForm):
    """Form for creating a new gloss from scratch"""
    class Meta:
        model = Gloss
        fields = ['idgloss', 'annotation_idgloss', 'sn']


class VideoUpdateForm(forms.Form):
    """Form to allow update of the video for a sign"""
    videofile = VideoUploadToFLVField()


class TagUpdateForm(forms.Form):
    """Form to add a new tag to a gloss"""

    tag = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), 
                            choices=[(t, t) for t in settings.ALLOWED_TAGS])
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput)

YESNOCHOICES = (("unspecified", "Unspecified" ), ('yes', 'Yes'), ('no', 'No'))
    
    
ROLE_CHOICES = [('all', 'All')]
ROLE_CHOICES.extend(defn_role_choices)

class GlossSearchForm(forms.ModelForm):
    
    search = forms.CharField(label="Search Gloss/SN")
    tags = forms.MultipleChoiceField(choices=[(t, t) for t in settings.ALLOWED_TAGS])
    nottags = forms.MultipleChoiceField(choices=[(t, t) for t in settings.ALLOWED_TAGS])
    keyword = forms.CharField(label='Keyword')
    hasvideo = forms.ChoiceField(label='Has Video', choices=YESNOCHOICES)
    defspublished = forms.ChoiceField(label="All Definitions Published", choices=YESNOCHOICES)
    
    defsearch = forms.CharField(label='Search Definition/Notes')
    defrole = forms.ChoiceField(label='Search Definition/Note Type', choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
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
        widgets = {
                   'inWeb': forms.Select(choices=YESNOCHOICES),
                   }
    

class DefinitionForm(forms.ModelForm):
    
    class Meta:
        model = Definition
        fields = ('count', 'role', 'text')
        widgets = {
                   'role': forms.Select(attrs={'class': 'form-control'}),
                   }

class RelationForm(forms.Form):
    
    sourceid = forms.CharField(label='Source Gloss')
    targetid = forms.CharField(label='Target Gloss')
    role = forms.ChoiceField(choices=[],widget=forms.Select(attrs={'class': 'form-control'})) 
    
    def __init__(self, *args, **kwargs):
        super(RelationForm, self).__init__(*args, **kwargs)
        choices = []
        for role in Relationrole.objects.all():
            if role.forwardmessage == role.backwardmessage:
                choices.append(('%s_bidirectional' % role.role, role.forwardmessage))
            else:
                choices.append(('%s_forward' % role.role, role.forwardmessage))
                choices.append(('%s_backward' % role.role, role.backwardmessage))
        self.fields['role'].choices = choices
    
    class Meta:
        model = Relation
        
        

        


