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
        return settings.MEDIA_URL
    except:
        return ''
 
    
@register.simple_tag
def auslan_static_prefix():
    """
    Returns the string contained in the setting AUSLAN_STATIC_PREFIX.
    """
    try:
        from django.conf import settings
        return settings.AUSLAN_STATIC_PREFIX 
    except:
        return ''
    
@register.simple_tag
def primary_css():
    """Return the primary css file basename from PRIMARY_CSS"""
    
    try:
        from django.conf import settings
        return settings.PRIMARY_CSS 
    except:
        return ''    
    
    
