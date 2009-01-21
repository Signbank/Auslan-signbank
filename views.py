from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404

from auslan.pages.views import page

def index(request):
    return page(request, '/')
     
