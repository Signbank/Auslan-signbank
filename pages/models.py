from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Page(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'pages/contact_page.html'. If this isn't provided, the system will use 'pages/default.html'."))
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)
    parent = models.ForeignKey('self', blank=True, null=True) 

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

class PageVideo(models.Model):
    page = models.ForeignKey('Page')
    title = models.CharField(_('title'), max_length=200)
    number = models.PositiveIntegerField(_('number'))
    video = models.FileField(upload_to=settings.PAGES_VIDEO_LOCATION, blank=True)
    
    def __unicode__(self):
        return "Page Video: %s" % (self.title,)