from auslan.pages.models import *
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'pages/default.html'

def page(request, url):
    """
    Flat page view.

    Models: `pages.page`
    Templates: Uses the template defined by the ``template_name`` field,
        or `pages/default.html` if template_name is not defined.
    Context:
        page
            `pages.page` object
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    # here I've removed the requirement that the page be for this site
    # - this won't work if we ever have more than one site here
    # which isn't planned
    f = get_object_or_404(Page, url__exact=url)
    
    
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.group_required:
        if not request.user.is_authenticated() :
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.path)
    
    # if there is a form var 'playlist' then generate a playlist
    # xml file instead of the page itself
    if request.GET.has_key('playlist'):
        return render_to_response('pages/playlist.xml', {'page': f}, mimetype='application/xml')
    
    
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, {
        'page': f,
        'menu': menu(),
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)
    return response

    
