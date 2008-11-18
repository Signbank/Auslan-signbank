from auslan.pages.models import Page


def menu(request):
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
    
    # return a dictionary to be merged with the request context
    return {'menu': menu}
    
    