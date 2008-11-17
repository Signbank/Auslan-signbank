from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404


def register(request):
    return render_to_response('register.html',
                              {'menuid':0, 'submenuid':0},
                              context_instance=RequestContext(request))

def index(request):
    return render_to_response('index.html',
                              {'menuid':1, 'submenuid':1},
                              context_instance=RequestContext(request))
    
#testing
 
def fingerspellingtwohanded(request):
    return render_to_response('fingerspell/fingerspellingtwohanded.html',
                              { 'menuid':3, 'submenuid':1, 'title':"The Two-Handed Alphabet"},
                              context_instance=RequestContext(request))

def fingerspellingonehanded(request):
    return render_to_response('fingerspell/fingerspellingonehanded.html',
                               { 'menuid':3, 'submenuid':2, 'title':"The American Sign Language One-Handed Alphabet"},
                              context_instance=RequestContext(request))

def numbersigns(request):
    return render_to_response('numbersigns/numbersigns.html',
                              { 'menuid':4, 'title':"Number Signs"},
                              context_instance=RequestContext(request))

