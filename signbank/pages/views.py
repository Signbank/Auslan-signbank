from signbank.pages.models import *
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.utils.safestring import mark_safe

DEFAULT_TEMPLATE = 'pages/default.html'

def page(request, url='/'):
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
    
    # deal with the lack of a root page
    try:
        f = Page.objects.get(url__exact=url)
    except:
        # no page, if we're after the root page then serve a default page
        if url == '/':

            f = Page(title='No Pages', 
                     content='<p>No pages defined. Login to <a href="/admin">admin</a> to create some.</p>')  
        else:
            t = loader.get_template("404.html")
            return HttpResponseNotFound(t.render(RequestContext(request))) 

    
    # If registration is required for accessing this page check the group
    if f.group_required:
        if request.user.is_authenticated():
            if not request.user.groups.filter(name=f.group_required.name).count():
                f = Page(title='Permission denied', 
                         content='<p>You do not have permission to access this page. This page is only available to users with the permission level of ' + f.group_required.name.lower() + '. If you believe you should have access to this page please send us <a href="/feedback/generalfeedback.html">feedback</a>.</p>')
        else:
            # Not logged in, redirect to the login page.
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.path)
    
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
    })
    response = HttpResponse(t.render(c))
    return response

    
