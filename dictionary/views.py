from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings 
from django.db.models import Q
import os

from signbank.dictionary.models import *
from signbank.dictionary.forms import * 
from signbank.feedback.models import *

def index(request, flavour='dictionary'):
    """Default view showing a browse/search entry
    point to the dictionary"""
    
    
    return render_to_response("dictionary/index.html",
                              {'flavour': flavour,
                               },
                               context_instance=RequestContext(request))



def word(request, viewname, keyword, n, flavour='dictionary'):
    """View of a single keyword that may have more than one sign"""

    n = int(n)

    if request.GET.has_key('feedbackmessage'):
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    word = get_object_or_404(Keyword, text=keyword)
    # returns (matching translation, number of matches) 
    (trans, total) =  word.match_request(request, n, flavour)
    
    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()
        
    videourl = trans.gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None
        
        
    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')

    # work out the number of this gloss and the total number    
    gloss = trans.gloss
    if request.user.is_staff:
        if flavour == 'medical':
            glosscount = Gloss.objects.filter(Q(healthtf__exact=True) | Q(InMedLex__exact=True)).count()
            glossposn = Gloss.objects.filter(Q(InMedLex__exact=True) | Q(healthtf__exact=True), sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
    else:
        if flavour == 'medical':
            glosscount = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True, sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1        
    
    # navigation gives us the next and previous signs
    nav = gloss.navigation(flavour, request.user.is_staff)
    
    # the gloss update form for staff
    update_form = None
    if request.user.is_authenticated() and request.user.is_staff:
        update_form = GlossUpdateForm(
                {'inWeb': trans.gloss.inWeb,
                 'inMedLex': trans.gloss.InMedLex,
                 'keyword': keyword,
                 'n': n,
                 'healthtf': trans.gloss.healthtf,
                 'bsltf': trans.gloss.bsltf,
                  })
        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'viewname': 'words',
                               'flavour': flavour,
                               'definitions': trans.gloss.definitions(),
                               'gloss': trans.gloss,
                               'allkwds': allkwds,
                               'n': n, 
                               'total': total, 
                               'matches': range(1, total+1),
                               'navigation': nav,
                               # lastmatch is a construction of the url for this word
                               # view that we use to pass to gloss pages
                               # could do with being a fn call to generate this name here and elsewhere
                               'lastmatch': str(trans.translation)+"-"+str(n),
                               'videofile': videourl,  
                               'update_form': update_form,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'feedback' : True,
                               'feedbackmessage': feedbackmessage,
                               },
                               context_instance=RequestContext(request))
  
    
def gloss(request, idgloss, flavour='dictionary'):
    """View of a gloss - mimics the word view, really for admin use
       when we want to preview a particular gloss"""

    gloss = Gloss.objects.get(idgloss=idgloss) 
    
    # and all the keywords associated with this sign
    allkwds = gloss.translation_set.all()
    if len(allkwds) == 0:
        trans = Translation()
    else:
        trans = allkwds[0]
        
    videourl = gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    if request.user.is_staff:
        if flavour == 'medical':
            glosscount = Gloss.objects.filter(Q(healthtf__exact=True) | Q(InMedLex__exact=True)).count()
            glossposn = Gloss.objects.filter(Q(InMedLex__exact=True) | Q(healthtf__exact=True), sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
    else:
        if flavour == 'medical':
            glosscount = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True, sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1    
        
    # navigation gives us the next and previous signs
    nav = gloss.navigation(flavour, request.user.is_staff)

    # the gloss update form for staff
    update_form = None
    if request.user.is_authenticated() and request.user.is_staff:
        update_form = GlossUpdateForm(
                {'inWeb': gloss.inWeb,
                 'inMedLex': gloss.InMedLex,
                 'healthtf': gloss.healthtf,
                 'bsltf': gloss.bsltf,
                  })    
    
    # get the last match keyword if there is one passed along as a form variable
    if request.GET.has_key('lastmatch'):
        lastmatch = request.GET['lastmatch']
    else:
        lastmatch = None
        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               'flavour': flavour,
                               'lastmatch': lastmatch,
                               'videofile': videourl,
                               'viewname': word,  
                               'feedback': None,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'navigation': nav,
                               'update_form': update_form,
                               },
                               context_instance=RequestContext(request))


from django.core.paginator import Paginator, InvalidPage

def search(request, flavour='dictionary'):
    """Handle keyword search form submission
    flavour is either 'dictionary' or 'medicalsignbank' and determines
    which part of the dictionary is searched"""
    
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    else:
        page = 1
    
    if request.GET.has_key('query'):
        # need to transcode the query to our encoding
        term = request.GET['query'] 
        try:
            term = term.encode("latin-1")
            
            # check the submitted 'msb' checkbox and change the flavour
            # as appropriate, do this by redirecting so that the page
            # url is correct always
            if request.GET.has_key('msb') and flavour == 'dictionary':
                newurl = request.path.replace('dictionary', 'medical') 
                return HttpResponseRedirect("%s?query=%s&msb=1" % (newurl, term))
            elif not request.GET.has_key('msb') and flavour == 'medical':
                newurl = request.path.replace('medical', 'dictionary') 
                return HttpResponseRedirect(newurl+"?query="+term)
            
            
            
            if request.user.is_authenticated() and request.user.is_staff: 
                # staff get to see all the words, but might be only medical
                if flavour == 'medical':
                    # select InMedLex OR healthtf to get all medical words
                    # remember InMedLex means 'Problematic Medical Sign'
                    # NOTE: dependancy with models.Keyword.match_request
                    words = Keyword.objects.filter(Q(text__istartswith=term),  
                                                   Q(translation__gloss__InMedLex__exact=True) |
                                                   Q(translation__gloss__healthtf__exact=True)).distinct()
                else: 
                    words = Keyword.objects.filter(text__istartswith=term)
            else:
                # regular users see either everything or health only signs
                if flavour == 'medical':
                    words = Keyword.objects.filter(text__istartswith=term,
                                                   translation__gloss__inWeb__exact=True,
                                                   translation__gloss__healthtf__exact=True).distinct()
                else:
                    words = Keyword.objects.filter(text__istartswith=term, 
                                                   translation__gloss__inWeb__exact=True).distinct()

        except:
            # if the encoding didn't work this is 
            # a strange unicode or other string
            # and it won't match anything in the dictionary 
            words = []
        
    else:
        term = ''
        words = []
        
    paginator = Paginator(words, 50) 
    

    # display the keyword page if there's only one hit
    if len(words) == 1:
        return HttpResponseRedirect('/'+flavour+'/words/'+words[0].text+'-1.html' ) 
        

    return render_to_response("dictionary/search_result.html",
                              {'query' : term, 
                               'paginator' : paginator, 
                               'page' : paginator.page(page), 
                               'menuid' : 2,
                               'flavour': flavour,
                               },
                              context_instance=RequestContext(request))



from django.db.models.loading import get_model, get_apps, get_models
from django.core import serializers

def keyword_value_list(request, prefix):
    """View to generate a list of possible values for 
    a keyword given a prefix."""
   

    kwds = Keyword.objects.filter(text__startswith=prefix)
    kwds_list = [k.text for k in kwds] 
    return HttpResponse("\n".join(kwds_list), content_type='text/plain')
    

def missing_video_list():
    """A list of signs that don't have an
    associated video file"""
    
    glosses = Gloss.objects.filter(inWeb__exact=True)
    for gloss in glosses:
        if not gloss.has_video():
            yield gloss

def missing_video_view(request, flavour):
    """A view for the above list"""
    
    glosses = missing_video_list()
    
    return render_to_response("dictionary/missingvideo.html",
                              {'glosses': glosses})


