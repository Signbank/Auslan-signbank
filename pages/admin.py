from django import forms
from django.contrib import admin
from auslan.pages.models import Page, PageVideo
from auslan.video.fields import VideoUploadToFLVField
from django.utils.translation import ugettext_lazy as _


class PageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = Page

   
class PageVideoForm(forms.ModelForm):
    video = VideoUploadToFLVField(label='Video',
                            required=True,
                            prefix='pages',
                            help_text = _("Uploaded video will be converted to Flash"),
                            widget = admin.widgets.AdminFileWidget)
    class Meta:
        model = PageVideo

    def save(self, commit=True):
        print "Saving a video form"
        print "VideoName: ", self.cleaned_data['video']
        print "cleaned data", self.cleaned_data
        instance = super(PageVideoForm, self).save(commit=commit)
        print "Instance:",  instance.video
        return instance

class PageVideoInline(admin.TabularInline):
    form = PageVideoForm
    model = PageVideo  
    extra = 1

class PageVideoAdmin(admin.ModelAdmin):
    model = PageVideo
    form = PageVideoForm
    
admin.site.register(PageVideo, PageVideoAdmin)

class PageAdmin(admin.ModelAdmin):
    form = PageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'parent')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [PageVideoInline]

admin.site.register(Page, PageAdmin)
