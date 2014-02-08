from django.template import Library

register = Library()

@register.simple_tag
def primary_css():
    """
    Returns the string contained in the setting PRIMARY_CSS - the
    prefix for any media served by the site
    """
    try:
        from django.conf import settings
        return settings.PRIMARY_CSS
    except:
        return ''
 
    