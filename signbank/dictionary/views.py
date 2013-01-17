from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tagging.models import Tag, TaggedItem

import os

from signbank.dictionary.models import *
from signbank.dictionary.forms import * 
from signbank.feedback.models import *

from signbank.video.forms import VideoUploadForGlossForm


def login_required_config(f):
    """like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True"""

    if settings.ALWAYS_REQUIRE_LOGIN:
        return login_required(f)
    else:
        return f



@login_required_config
def index(request, version='dictionary'):
    """Default view showing a browse/search entry
    point to the dictionary"""
    
    
    return render_to_response("dictionary/search_result.html",
                              {'version': version,
                               'query': '',
                               },
                               context_instance=RequestContext(request))


def taglist(request, tag=None, version='dictionary'):
    """View of a list of tags or a list of signs with a given tag"""

    
    if tag:
        # get the glosses with this tag
        tagobj = get_object_or_404(Tag, name=tag)
        gloss_list = TaggedItem.objects.get_by_model(Gloss, tagobj)
        
        if ':' in tag:
            taginfo = tag.split(':')
        else:
            taginfo = ('None', tag)
    
        if request.GET.has_key('page'):
            page = int(request.GET['page'])
        else:
            page = 1
        
        paginator = Paginator(gloss_list, 50) 
        
        return render_to_response('dictionary/gloss_list.html',
                                  {'paginator': paginator,
                                   'page': paginator.page(page),
                                   'thistag': taginfo,
                                   'tagdict': tag_dict(),
                                   'version': version},
                                   context_instance=RequestContext(request) )
    else:
        return render_to_response('dictionary/gloss_list.html',
                                  {'version': version,
                                   'tagdict': tag_dict(),
                                   },
                                   context_instance=RequestContext(request))


def tag_dict():
    """Generate a dictionary of tags categorised by their
    category (the part before the colon)"""
    
    tags = Tag.objects.usage_for_model(Gloss, counts=True)
    # build a dictionary of tags under their categories
    cats = dict()
    for tag in tags:
        if tag.name.find(':') >= 0:
            (cat, tagname) = tag.name.split(":", 1)
        else:
            cat = "None"
            tagname = tag.name
            
        if cats.has_key(cat):
            cats[cat].append((tagname, tag.count))
        else:
            cats[cat] = [(tagname, tag.count)]
    
    return cats


STATE_IMAGES = {'auslan_all': "images/maps/allstates.gif",
                'auslan_nsw_act_qld': "images/maps/nsw-act-qld.gif",
                'auslan_nsw': "images/maps/nsw.gif",
                'auslan_nt':  "images/maps/nt.gif",
                'auslan_qld': "images/maps/qld.gif",
                'auslan_sa': "images/maps/sa.gif",
                'auslan_tas': "images/maps/tas.gif",
                'auslan_south': "images/maps/vic-wa-tas-sa-nt.gif",
                'auslan_vic': "images/maps/vic.gif",
                'auslan_wa': "images/maps/wa.gif",
                }

def map_image_for_dialects(dialects):
    """Get the right map image for this dialect set
    
    
    Relies on database contents, which is bad. This should
    be in the database
    """
    # we only work for Auslan just now
    dialects = dialects.filter(language__name__exact="Auslan")

    if len(dialects) == 0:
        return 
    
    # all states 
    if dialects.filter(name__exact="Australia Wide"):
        return STATE_IMAGES['auslan_all']
    
    if dialects.filter(name__exact="Southern Dialect"):
        return STATE_IMAGES['auslan_south']
    
    if dialects.filter(name__exact="Northern Dialect"):
        return STATE_IMAGES['auslan_nsw_act_qld']
    
    if dialects.filter(name__exact="New South Wales"):
        return STATE_IMAGES['auslan_nsw']    
    
    if dialects.filter(name__exact="Queensland"):
        return STATE_IMAGES['auslan_qld']    
    
    if dialects.filter(name__exact="Western Australia"):
        return STATE_IMAGES['auslan_wa']

    if dialects.filter(name__exact="South Australia"):
        return STATE_IMAGES['auslan_sa']
    
    if dialects.filter(name__exact="Tasmania"):
        return STATE_IMAGES['auslan_tas']    
    
    if dialects.filter(name__exact="Victoria"):
        return STATE_IMAGES['auslan_vic']

    return None


@login_required_config
def word(request, viewname, keyword, n, version='dictionary'):
    """View of a single keyword that may have more than one sign"""

    n = int(n)

    if request.GET.has_key('feedbackmessage'):
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False

    word = get_object_or_404(Keyword, text=keyword)
    # returns (matching translation, number of matches) 
    (trans, total) =  word.match_request(request, n, version)
    
    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()
        
    videourl = trans.gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None
    
    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')

    # work out the number of this gloss and the total number    
    gloss = trans.gloss
    if request.user.is_staff:
        if version == 'medical':
            glosscount = Gloss.objects.filter(Q(healthtf__exact=True) | Q(InMedLex__exact=True)).count()
            glossposn = Gloss.objects.filter(Q(InMedLex__exact=True) | Q(healthtf__exact=True), sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
    else:
        if version == 'medical':
            glosscount = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True, sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1        
    
    # navigation gives us the next and previous signs
    nav = gloss.navigation(version, request.user.is_staff)
    
    # the gloss update form for staff

    if request.user.is_authenticated() and request.user.is_staff:
        update_form = GlossModelForm(instance=trans.gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_sn': trans.gloss.sn,
                                                      'redirect': request.path})
    else:
        update_form = None
        video_form = None

        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'viewname': 'words',
                               'version': version,
                               'definitions': trans.gloss.definitions(),
                               'gloss': trans.gloss,
                               'allkwds': allkwds,
                               'n': n, 
                               'total': total, 
                               'matches': range(1, total+1),
                               'navigation': nav,
                               'dialect_image': map_image_for_dialects(gloss.dialect.all()),
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
                               },
                               context_instance=RequestContext(request))
  
@login_required_config
def gloss(request, idgloss, version='dictionary'):
    """View of a gloss - mimics the word view, really for admin use
       when we want to preview a particular gloss"""

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

    if request.user.is_staff:
        if version == 'medical':
            glosscount = Gloss.objects.filter(Q(healthtf__exact=True) | Q(InMedLex__exact=True)).count()
            glossposn = Gloss.objects.filter(Q(InMedLex__exact=True) | Q(healthtf__exact=True), sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
    else:
        if version == 'medical':
            glosscount = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, healthtf__exact=True, sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, sn__lt=gloss.sn).count()+1    
        
    # navigation gives us the next and previous signs
    nav = gloss.navigation(version, request.user.is_staff)

    # the gloss update form for staff
    update_form = None
    
    if request.user.is_authenticated() and request.user.is_staff:
        update_form = GlossModelForm(instance=gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_sn': gloss.sn,
                                                      'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None
    
    
    
    # get the last match keyword if there is one passed along as a form variable
    if request.GET.has_key('lastmatch'):
        lastmatch = request.GET['lastmatch']
    else:
        lastmatch = None
        
    return render_to_response("dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               'dialect_image': map_image_for_dialects(gloss.dialect.all()),
                               'version': version,
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
                               },
                               context_instance=RequestContext(request))


from django.core.paginator import Paginator, InvalidPage

@login_required_config
def search(request, version='dictionary'):
    """Handle keyword search form submission
    version is either 'dictionary' or 'medicalsignbank' and determines
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
            
            # check the submitted 'msb' checkbox and change the version
            # as appropriate, do this by redirecting so that the page
            # url is correct always
            if request.GET.has_key('msb') and version == 'dictionary':
                newurl = request.path.replace('dictionary', 'medical') 
                return HttpResponseRedirect("%s?query=%s&msb=1" % (newurl, term))
            elif not request.GET.has_key('msb') and version == 'medical':
                newurl = request.path.replace('medical', 'dictionary') 
                return HttpResponseRedirect(newurl+"?query="+term)
            
            
            
            if request.user.is_authenticated() and request.user.is_staff: 
                # staff get to see all the words, but might be only medical
                if version == 'medical':
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
                if version == 'medical':
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
        return HttpResponseRedirect('/'+version+'/words/'+words[0].text+'-1.html' ) 
        

    return render_to_response("dictionary/search_result.html",
                              {'query' : term, 
                               'paginator' : paginator, 
                               'wordcount' : len(words),
                               'page' : paginator.page(page), 
                               'menuid' : 2,
                               'version': version,
                               },
                              context_instance=RequestContext(request))



from django.db.models.loading import get_model, get_apps, get_models
from django.core import serializers

def keyword_value_list(request, prefix=None, version='dictionary'):
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

def missing_video_view(request, version):
    """A view for the above list"""
    
    glosses = missing_video_list()
    
    return render_to_response("dictionary/missingvideo.html",
                              {'glosses': glosses})


## csv export
import csv

def csv_export(request, version):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dictionary-export.csv"'


    fields = ['sn', 'idgloss', 'annotation_idgloss', 'morph', 'tags']

    writer = csv.writer(response)
    header = [Gloss._meta.get_field(f).verbose_name for f in fields]
    header.append("Translations")
    writer.writerow(header)
    
    for gloss in Gloss.objects.all():
        row = []
        for f in fields:
            row.append(getattr(gloss, f))
            
        trans = [t.translation.text for t in gloss.translation_set.all()]
        row.append(", ".join(trans))
            
        writer.writerow(row)

    return response



