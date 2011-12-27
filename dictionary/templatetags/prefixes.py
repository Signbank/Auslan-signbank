from django.template import Library

register = Library()

@register.simple_tag
def auslan_media_prefix():
    """
    Returns the string contained in the setting MEDIA_URL - the
    prefix for any media served by the site
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
 
    
@register.simple_tag
def auslan_static_prefix():
    """
    Returns the string contained in the setting AUSLAN_STATIC_PREFIX.
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.AUSLAN_STATIC_PREFIX 
    
    
