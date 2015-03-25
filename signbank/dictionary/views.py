from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tagging.models import Tag, TaggedItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe

from django.utils.encoding import smart_unicode

import os

from signbank.dictionary.models import *
from signbank.dictionary.forms import *
from signbank.feedback.models import *
from signbank.pages.models import *

from signbank.video.forms import VideoUploadForGlossForm


def login_required_config(f):
    """like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True"""

    if settings.ALWAYS_REQUIRE_LOGIN:
        return login_required(f)
    else:
        return f



@login_required_config
def index(request):
    """Default view showing a browse/search entry
    point to the dictionary"""


    return render_to_response("dictionary/search_result.html",
                              {'form': UserSignSearchForm(),
                               'language': settings.LANGUAGE_NAME,
                               'query': '',
                               },
                               context_instance=RequestContext(request))



def map_image_for_regions(regions):
    """Get the right map images for this region set
    """
    
    # Add a map for every unique language and dialect we have
    # regional information on
    # This may look odd if there is more than one language
    images = []
    for region in regions.all():
        language_name = region.dialect.language.name.replace(" ", "")
        dialect_name = region.dialect.name.replace(" ", "")
        dialect_extension = ""
        if region.traditional:
            dialect_extension = "-traditional"
        
        language_filename = "images/maps/" + language_name + ".png"
        dialect_filename = "images/maps/" + language_name + "/" + dialect_name + dialect_extension + ".png"
        
        if language_filename not in images:
            images.append(language_filename)
        if dialect_filename not in images:
            images.append(dialect_filename)
        
    return images
    

@login_required_config
def word_and_regional_view(request, keyword, n, viewname):
    """
    Helper view that displays the word or the regional view depending on what
    viewname is set to
    """

    n = int(n)

    if request.GET.has_key('feedbackmessage'):
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    word = get_object_or_404(Keyword, text=keyword)

    # returns (matching translation, number of matches)
    (trans, total) =  word.match_request(request, n, )

    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()

    videourl = trans.gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')

    # work out the number of this gloss and the total number
    gloss = trans.gloss
    if gloss.sn != None:
        if request.user.has_perm('dictionary.search_gloss'):
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1
    else:
        glosscount = 0
        glossposn = 0

    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))

    # the gloss update form for staff

    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=trans.gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_id': trans.gloss.pk,
                                                      'redirect': request.path})
    else:
        update_form = None
        video_form = None

    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None
        
    # If we asked for a regional view but there is no regional information available fall over
    if viewname == "regional" and len(regions) == 0:
        raise Http404

    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'viewname': viewname,
                               'definitions': trans.gloss.definitions(),
                               'gloss': trans.gloss,
                               'allkwds': allkwds,
                               'n': n,
                               'total': total,
                               'matches': range(1, total+1),
                               'navigation': nav,
                               'dialect_image': map_image_for_regions(gloss.region_set),
                               'regions': regions,
                               'regional_template_content': regional_template_content,
                               # lastmatch is a construction of the url for this word
                               # view that we use to pass to gloss pages
                               # could do with being a fn call to generate this name here and elsewhere
                               'lastmatch': str(trans.translation)+"-"+str(n),
                               'videofile': videourl,
                               'update_form': update_form,
                               'videoform': video_form,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'feedback' : True,
                               'feedbackmessage': feedbackmessage,
                               'tagform': TagUpdateForm(),
                               'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                               'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                               },
                               context_instance=RequestContext(request))

@login_required_config
def word(request, keyword, n):
    """View of a single keyword that may have more than one sign"""
    
    return word_and_regional_view(request, keyword, n, "words")

@login_required_config
def regional(request, keyword, n):
    """View of a single keyword that may have more than one sign alongside regional information"""
    
    return word_and_regional_view(request, keyword, n, "regional")

@login_required_config
def gloss(request, idgloss):
    """View of a gloss - mimics the word view, really for admin use
       when we want to preview a particular gloss"""


    if request.GET.has_key('feedbackmessage'):
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    # we should only be able to get a single gloss, but since the URL
    # pattern could be spoofed, we might get zero or many
    # so we filter first and raise a 404 if we don't get one
    glosses = Gloss.objects.filter(idgloss=idgloss)

    if len(glosses) != 1:
        raise Http404

    gloss = glosses[0]

    # and all the keywords associated with this sign
    allkwds = gloss.translation_set.all()
    if len(allkwds) == 0:
        trans = Translation()
    else:
        trans = allkwds[0]

    videourl = gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None

    if gloss.sn != None:
        if request.user.has_perm('dictionary.search_gloss'):
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1
    else:
        glosscount = 0
        glossposn = 0

    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))

    # the gloss update form for staff
    update_form = None

    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_id': gloss.pk,
                                                      'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None



    # get the last match keyword if there is one passed along as a form variable
    if request.GET.has_key('lastmatch'):
        lastmatch = request.GET['lastmatch']
        if lastmatch == "None":
            lastmatch = False
    else:
        lastmatch = False

    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None

    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               'dialect_image': map_image_for_regions(gloss.region_set),
                               'regions': regions,
                               'regional_template_content': regional_template_content,
                               'lastmatch': lastmatch,
                               'videofile': videourl,
                               'viewname': word,
                               'feedback': None,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'navigation': nav,
                               'update_form': update_form,
                               'videoform': video_form,
                               'tagform': TagUpdateForm(),
                               'feedbackmessage': feedbackmessage,
                               'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                               'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                               },
                               context_instance=RequestContext(request))



@login_required_config
def search(request):
    """Handle keyword search form submission"""

    form = UserSignSearchForm(request.GET.copy())

    if form.is_valid():
        # need to transcode the query to our encoding
        term = form.cleaned_data['query']
        category = form.cleaned_data['category']
        
        # safe search for authenticated users if the setting says so
        safe = (not request.user.is_authenticated()) and settings.ANON_SAFE_SEARCH

        try:
            term = smart_unicode(term)
        except:
            # if the encoding didn't work this is
            # a strange unicode or other string
            # and it won't match anything in the dictionary
            words = []

        if request.user.has_perm('dictionary.search_gloss'):
            # staff get to see all the words that have at least one translation
            words = Keyword.objects.filter(text__istartswith=term, translation__isnull=False).distinct()
        else:
            # regular users see either everything that's published
            words = Keyword.objects.filter(text__istartswith=term,
                                            translation__gloss__inWeb__exact=True).distinct()

        try:
            crudetag = Tag.objects.get(name='lexis:crude')
        except:
            crudetag = None
        
        if safe and crudetag != None:
            
            crude = TaggedItem.objects.get_by_model(Gloss, crudetag)
            # remove crude words from result

            result = []
            for w in words:
                # remove word if all glosses for any translation are tagged crude
                trans = w.translation_set.all()
                glosses = [t.gloss for t in trans]
                
                if not all([g in crude for g in glosses]):
                    result.append(w)
            
            words = result
            
            
        if not category in ['all', '']:
            
            tag = Tag.objects.get(name=category)
            
            result = []
            for w in words:
                trans = w.translation_set.all()
                glosses = [t.gloss for t in trans]
                for g in glosses:
                    if tag in g.tags:
                        result.append(w)
            words = result


    else:
        term = ''
        words = []


    # display the keyword page if there's only one hit and it is an exact match
    if len(words) == 1 and words[0].text == term:
        return HttpResponseRedirect('/dictionary/words/'+words[0].text+'-1.html' )

    paginator = Paginator(words, 50)
    if request.GET.has_key('page'):
        
        page = request.GET['page']
        try:
            result_page = paginator.page(page)
        except PageNotAnInteger:
            result_page = paginator.page(1)
        except EmptyPage:
            result_page = paginator.page(paginator.num_pages)

    else:
        result_page = paginator.page(1)



    return render_to_response("dictionary/search_result.html",
                              {'query' : term,
                               'form': form,
                               'paginator' : paginator,
                               'wordcount' : len(words),
                               'page' : result_page,
                               'ANON_SAFE_SEARCH': settings.ANON_SAFE_SEARCH,                                         
                               'ANON_TAG_SEARCH': settings.ANON_TAG_SEARCH,
                               'language': settings.LANGUAGE_NAME,
                               },
                              context_instance=RequestContext(request))



from django.db.models.loading import get_model, get_apps, get_models
from django.core import serializers

def keyword_value_list(request, prefix=None):
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

def missing_video_view(request):
    """A view for the above list"""

    glosses = missing_video_list()

    return render_to_response("dictionary/missingvideo.html",
                              {'glosses': glosses})



