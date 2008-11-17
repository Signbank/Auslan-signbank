from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Group



class Page(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'pages/contact_page.html'. If this isn't provided, the system will use 'pages/default.html'."))
    publish = models.BooleanField(_('publish'), help_text=_("If this is checked, the page will be included in the site menus."))
    parent = models.ForeignKey('self', blank=True, null=True, help_text=_("Leave blank for a top level menu entry"))     

    group_required = models.ForeignKey(Group, null=True, blank=True, help_text=_("This page will only be visible to members of this group, leave blank to allow anyone to access."))

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
    
def menu():
    """Generate a menu hierarchy from the current set of pages"""
    
    menu = {'home': [], 'toplevel': []}

    # home is the page titled 'Home'
    homes = Page.objects.filter(title="Home")
    if len(homes) >= 1:
        home = homes[0]
        for page in Page.objects.filter(parent=home):
            menu['home'].append({'url': page.url, 'title': page.title})
    else:
        home = None
    # find toplevel pages, with no parent
    toplevel = Page.objects.filter(parent=None)
    for page in toplevel:
        if page != home:
            menu['toplevel'].append({'url': page.url, 'title': page.title})
        
    return menu
    
    
    
