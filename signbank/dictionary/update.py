from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from signbank.log import debug
from tagging.models import TaggedItem, Tag
import os, shutil

from signbank.dictionary.models import *
from signbank.dictionary.forms import *

def add_gloss(request):
    """Create a new gloss and redirect to the edit view"""
    
    if request.method == "POST":
        
        form = GlossCreateForm(request.POST)
        if form.is_valid():
            
            gloss = form.save()
            
            return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id}))
        
    return HttpResponseRedirect(reverse('dictionary:admin_gloss_list'))


def update_gloss(request, glossid):
    """View to update a gloss model from the jeditable jquery form
    We are sent one field and value at a time, return the new value
    once we've updated it."""

    if not request.user.has_perm('dictionary.change_gloss'):
        return HttpResponseForbidden("Gloss Update Not Allowed")

    if request.method == "POST":

        gloss = get_object_or_404(Gloss, id=glossid)

        field = request.POST.get('id', '')
        value = request.POST.get('value', '')
        values = request.POST.getlist('value[]')   # in case we need multiple values 
        
        # validate
        # field is a valid field
        # value is a valid value for field
        
        if field == 'deletegloss':
            if value == 'confirmed':
                # delete the gloss and redirect back to gloss list
                gloss.delete()
                return HttpResponseRedirect(reverse('dictionary:admin_gloss_list'))
        
        if field.startswith('definition'):
            
            (what, defid) = field.split('_')
            try:
                defn = Definition.objects.get(id=defid)
            except:
                return HttpResponseBadRequest("Bad Definition ID '%s'" % defid, {'content-type': 'text/plain'})
        
            if not defn.gloss == gloss:
                return HttpResponseBadRequest("Definition doesn't match gloss", {'content-type': 'text/plain'})
            
            if what == 'definitiondelete':
                defn.delete()
                return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id}))
            
            if what == 'definition':
                # update the definition
                defn.text = value
                defn.save()
                newvalue = defn.text
            elif what == 'definitioncount':
                defn.count = int(value)
                defn.save()
                newvalue = defn.count
            elif what == 'definitionpub':
                print "PUB:", value
                defn.published = value == 'Yes'
                defn.save()
                if defn.published:
                    newvalue = 'Yes'
                else:
                    newvalue = 'No'
            elif what == 'definitionrole':
                defn.role = value
                defn.save()
                newvalue = defn.get_role_display()
                
                
        elif field == 'keywords':
            kwds = [k.strip() for k in value.split(',')]
            # remove current keywords 
            current_trans = gloss.translation_set.all()
            #current_kwds = [t.translation for t in current_trans]
            current_trans.delete()
            # add new keywords
            for i in range(len(kwds)):
                (kobj, created) = Keyword.objects.get_or_create(text=kwds[i])
                trans = Translation(gloss=gloss, translation=kobj, index=i)
                trans.save()
            
            newvalue = ", ".join([t.translation.text for t in gloss.translation_set.all()])
            
        elif field == 'language':
            # expecting possibly multiple values

            try:
                gloss.language.clear()
                for value in values:
                    lang = Language.objects.get(name=value)
                    gloss.language.add(lang)
                gloss.save()
                newvalue = ", ".join([str(g) for g in gloss.language.all()])
            except:                
                return HttpResponseBadRequest("Unknown Language %s" % values, {'content-type': 'text/plain'})
                
        elif field == 'dialect':
            # expecting possibly multiple values

            try:
                gloss.dialect.clear()
                for value in values:
                    lang = Dialect.objects.get(name=value)
                    gloss.dialect.add(lang)
                gloss.save()
                newvalue = ", ".join([str(g.name) for g in gloss.dialect.all()])
            except:                
                return HttpResponseBadRequest("Unknown Dialect %s" % values, {'content-type': 'text/plain'})
                
        elif field == "sn":
            # sign number must be unique, return error message if this SN is 
            # already taken
            
            if value == '':
                gloss.__setattr__(field, None)
                gloss.save()
                newvalue = ''
            else:
                try:
                    value = int(value)
                except:
                    return HttpResponseBadRequest("SN value must be integer", {'content-type': 'text/plain'})
                
                existing_gloss = Gloss.objects.filter(sn__exact=value)
                if existing_gloss.count() > 0:
                    g = existing_gloss[0].idgloss
                    return HttpResponseBadRequest("SN value already taken for gloss %s" % g, {'content-type': 'text/plain'})
                else:
                    gloss.sn = value
                    gloss.save()
                    newvalue = value
            
        
        else:
            

            if not field in Gloss._meta.get_all_field_names():
                return HttpResponseBadRequest("Unknown field", {'content-type': 'text/plain'})
            
            # special cases 
            # - Foreign Key fields (Language, Dialect)
            # - keywords
            # - videos
            # - tags
            
            # special value of 'notset' or -1 means remove the value
            if value == 'notset' or value == -1 or value == '':
                gloss.__setattr__(field, None)
                gloss.save()
                newvalue = ''
            else: 
            
                gloss.__setattr__(field, value)
                gloss.save()
                
                f = Gloss._meta.get_field(field)
                
                
                # for choice fields we want to return the 'display' version of 
                # the value
                valdict = dict(f.flatchoices)
                # some fields take ints
                if valdict.keys() != [] and type(valdict.keys()[0]) == int:
                    newvalue = valdict.get(int(value), value)
                else:
                    # either it's not an int or there's no flatchoices
                    # so here we use get with a default of the value itself
                    newvalue = valdict.get(value, value)
        
        return HttpResponse(newvalue, {'content-type': 'text/plain'})


def add_definition(request, glossid):
    """Add a new definition for this gloss"""
    
    
    thisgloss = get_object_or_404(Gloss, id=glossid)
    
    if request.method == "POST":
        form = DefinitionForm(request.POST)
        
        if form.is_valid():
            
            
            count = form.cleaned_data['count']
            role = form.cleaned_data['role']
            text = form.cleaned_data['text']
            
            # create definition, default to not published
            defn = Definition(gloss=thisgloss, count=count, role=role, text=text, published=False)
            defn.save()
            
    return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': thisgloss.id}))


def add_tag(request, glossid):
    """View to add a tag to a gloss"""

    # default response
    response = HttpResponse('invalid', {'content-type': 'text/plain'})

    if request.method == "POST":
        thisgloss = get_object_or_404(Gloss, id=glossid)

        form = TagUpdateForm(request.POST)
        if form.is_valid():

            tag = form.cleaned_data['tag']

            if form.cleaned_data['delete']:
                # get the relevant TaggedItem
                ti = get_object_or_404(TaggedItem, object_id=thisgloss.id, tag=tag)
                ti.delete()
                response = HttpResponse('deleted', {'content-type': 'text/plain'})
            else:
                # we need to wrap the tag name in quotes since it might contain spaces
                Tag.objects.add_tag(thisgloss, '"%s"' % tag)
                # response is new HTML for the tag list and form
                response = render_to_response('dictionary/glosstags.html',
                                              {'gloss': thisgloss,
                                               'tagform': TagUpdateForm(),
                                               },
                                              context_instance=RequestContext(request))
                
    return response





