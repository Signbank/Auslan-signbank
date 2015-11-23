from signbank.pages.models import Page
from django.conf import settings

def menu(request):
    """Generate a menu hierarchy from the current set of pages
    
    Returns a list of toplevel menu entries
    which are lists of dictionaries each with
    keys 'url', 'title' and 'children', the value of 'children'
    is a similar list of dictionaries.
    """
    
    # find toplevel pages, with no parent and thier children
    (menu, ignore) = find_children(None, request.META['PATH_INFO']) 
    # return a dictionary to be merged with the request context
    return {'menu': menu}
    

def find_children(page, currentURL):
    """Find the child pages of a given page,
    return a list of dictionaries suitable for insertion
    into the menu structure described in menu()"""

    isCurrent = False
    anyCurrent = False
    result = []
    for page in Page.objects.filter(parent=page, publish=True).order_by('index'):
        (children, childCurrent) = find_children(page, currentURL)
        # we're the current page if any of our children are the current page
        # or if we're the current page        
        isCurrent = ((page.url==currentURL) or childCurrent)
        
        # remember if any of the children are the current page
        anyCurrent = (isCurrent or anyCurrent)
        result.append({'url': page.url, 'title': page.title, 'children': children, 'current': isCurrent})

    return (result, anyCurrent)
    
def configuration(request):
    """
    Return settings that can be used in the templates
    """
    
    return {
       'settings_site_title': settings.SITE_TITLE,
       'settings_admin_email': settings.ADMIN_EMAIL,
       'settings_google_analytics_tracking_code': settings.GOOGLE_ANALYTICS_TRACKING_CODE,
       'settings_social_network_share_links': settings.SOCIAL_NETWORK_SHARE_LINKS,
       'settings_social_network_facebook_page': settings.SOCIAL_NETWORK_FACEBOOK_PAGE,
       'settings_social_network_facebook_share': settings.SOCIAL_NETWORK_FACEBOOK_SHARE,
       'settings_social_network_twitter_page': settings.SOCIAL_NETWORK_TWITTER_PAGE,
       'settings_social_network_twitter_share': settings.SOCIAL_NETWORK_TWITTER_SHARE,
       'settings_number_signs': settings.NUMBER_SIGNS,
       'settings_colour_signs': settings.COLOUR_SIGNS,
       'settings_country_signs': settings.COUNTRY_SIGNS,
       'settings_place_signs': settings.PLACE_SIGNS,
       'settings_finger_signs': settings.FINGER_SIGNS,
    }