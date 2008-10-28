from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings 

import os

from auslan.dictionary.models import *
from auslan.dictionary.forms import * 
from auslan.feedback.models import *

def word(request, viewname, keyword, n):
 
    """View of a single keyword that may have more than one sign"""
    
    n = int(n)
    
    word = get_object_or_404(Keyword, text=keyword)
    
    if request.user.is_authenticated() and request.user.is_staff:
        alltrans = word.translation_set.all()
    else:
        alltrans = word.translation_set.filter(gloss__inWeb__exact=True)
    
    # if there are no translations, return a 
    # special error page
    if len(alltrans) == 0:
        raise Http404
        
    
    # take the nth translation if n is in range
    # otherwise take the last
    if n-1 < len(alltrans):
        trans = alltrans[n-1]
    else:
        trans = alltrans[len(alltrans)-1] 
    
    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()
    
    # remember that n is one indexed
    if n>1:
        prev = n-1
    else:
        prev = None
        
    if n < len(alltrans):
        next = n+1
    else:
        next = None
        
    
    videourl = trans.gloss.get_video_url()
    
    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')
    
    # need to assert login for the feedback form
    valid = False
    if viewname == "feedback":
        if request.user.is_authenticated():
 
            
            if request.method == "POST":
                feedback_form = SignFeedbackForm(request.POST)
                
                if feedback_form.is_valid():
                    # get the clean (normalised) data from the feedback_form
                    clean = feedback_form.cleaned_data
                    # create a SignFeedback object to store the result in the db
                    sfb = SignFeedback(
                        isAuslan=clean['isAuslan'],
                        whereused=clean['whereused'],
                        like=clean['like'],
                        use=clean['use'],
                        suggested=clean['suggested'],
                        correct=clean['correct'],
                        kwnotbelong=clean['kwnotbelong'],
                        comment=clean['comment'],
                        user=request.user,
                        translation_id = request.POST["translation_id"]
                        )
                    sfb.save()
                    valid = True 
            else:
                feedback_form = SignFeedbackForm()
        else:
            # feedback requested but user is not logged in
            # redirect to the login page
            # return HttpResponseRedirect("/accounts/login/?next="+reverse('auslan.dictionary.views.word', args=[viewname, keyword, n]))
            # using reverse would be good here but the current implementation borks on 
            # the nested parens in the RE for this view
            return HttpResponseRedirect("/accounts/login/?next=/dictionary/feedback/"+keyword+"-"+str(n)+".html")
    else:
        feedback_form = False
        
    # the gloss update form for staff
    update_form = None
    if request.user.is_authenticated() and request.user.is_staff:
        update_form = GlossUpdateForm(
                {'inWeb': trans.gloss.inWeb,
                 'inMedLex': trans.gloss.InMedLex,
                 'keyword': keyword,
                 'n': n,
                  })
        
        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': trans.gloss.definitions(),
                               'gloss': trans.gloss,
                               'allkwds': allkwds,
                               'n': n, 
                               'total': len(alltrans),
                               'prev': prev,
                               'next': next,
                               'menuid': 2,
                               'videofile': videourl,
                               'viewname': viewname,
                               'feedback_form': feedback_form,
                               'update_form': update_form,
                               'valid': valid,
                               'feedback': trans.signfeedback_set.all()
                               },
                               context_instance=RequestContext(request))
    
    
def viewfeedback(request, keyword, n):
    """View feedback currently collected for this keyword"""

    
    n = int(n)
    word = Keyword.objects.get(text=keyword)
    if request.user.is_authenticated() and request.user.is_staff:
        alltrans = word.translation_set.all()
    else:
        alltrans = word.translation_set.filter(gloss__inWeb__exact=True)
    
    # take the nth translation if n is in range
    # otherwise take the last
    if n-1 < len(alltrans):
        trans = alltrans[n-1]
    else:
        trans = alltrans[len(alltrans)-1] 
    
    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()
    
    # remember that n is one indexed
    if n>1:
        prev = n-1
    else:
        prev = None
        
    if n < len(alltrans):
        next = n+1
    else:
        next = None
        
     
    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')
    
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': trans.gloss.definitions(),
                               'gloss': trans.gloss,
                               'allkwds': allkwds,
                               'n': n, 
                               'total': len(alltrans),
                               'prev': prev,
                               'next': next,
                               'menuid': 2,
                               'videofile': trans.gloss.get_video_url(),
                               'viewname': 'viewfeedback',
                               'feedback_form': None,
                               'update_form': None,
                               'valid': True,
                               'feedback': trans.signfeedback_set.all()
                               },
                               context_instance=RequestContext(request))
    
    
    
def gloss(request, idgloss):
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
 
        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               'n': 1, 
                               'total': 1,
                               'prev': 1,
                               'next': 1,
                               'menuid': 2,
                               'videofile': videourl,
                               'viewname': word, 
                               'valid': True,
                               'feedback': None,
                               'gloss': gloss,
                               },
                               context_instance=RequestContext(request))
        

from django.core.paginator import Paginator, InvalidPage

def search(request):
    """Handle keyword search form submission"""
    
    if request.GET.has_key('page'):
        page = int(request.GET['page'])
    else:
        page = 1
    
    if request.GET.has_key('query'):
        # need to transcode the query to our encoding
        term = request.GET['query'] 
        try:
            term = term.encode("latin-1")
            
            if request.user.is_authenticated() and request.user.is_staff:
                # staff get to see all the words
                words = Keyword.objects.filter(text__istartswith=term)
            else:
                # get only the keywords that are in the Web edition
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
        
    paginator = Paginator(words, 17*3) 
    

    # display the keyword page if there's only one hit
    if len(words) == 1:
        return HttpResponseRedirect('/dictionary/words/'+words[0].text+'-1.html' ) 
        

    return render_to_response("dictionary/search_result.html",
                              {'query' : term, 
                               'paginator' : paginator, 
                               'page' : paginator.page(page), 
                               'menuid' : 2,
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
    
