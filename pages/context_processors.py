from auslan.pages.models import Page


def menu(request):
    """Generate a menu hierarchy from the current set of pages
    
    Returns a dictionary with keys 'home' and 'toplevel', the
    entries of these are lists of dictionaries each with
    keys 'url', 'title' and 'children', the value of 'children'
    is a similar list of dictionaries.
    """
    
    menu = {'home': [], 'toplevel': []}

    # home is the page titled 'Home'
    homes = Page.objects.filter(title="Home")
    if len(homes) >= 1:
        home = homes[0]
        menu['home'] = find_children(home)
    else:
        home = None
    # find toplevel pages, with no parent
    menu['toplevel'] = find_children(None)
    
    # return a dictionary to be merged with the request context
    return {'menu': menu}
    

def find_children(page):
    """Find the child pages of a given page,
    return a list of dictionaries suitable for insertion
    into the menu structure described in menu()"""
    
    result = []
    for page in Page.objects.filter(parent=page, publish=True):
        if not page.title == "Home":
            result.append({'url': page.url, 'title': page.title, 'children': find_children(page)})
            
    return result
    
    