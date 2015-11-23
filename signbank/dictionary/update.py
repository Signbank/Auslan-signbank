from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.template import Context, RequestContext, loader
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from signbank.log import debug
from tagging.models import TaggedItem, Tag
import os, shutil, re

from signbank.dictionary.models import *
from signbank.dictionary.forms import *

@permission_required('dictionary.add_gloss')
def add_gloss(request):
    """Create a new gloss and redirect to the edit view"""
    
    if request.method == "POST":
        
        form = GlossCreateForm(request.POST)
        if form.is_valid():
            
            gloss = form.save()
            
            return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id})+'?edit')
        else:
            return render_to_response('dictionary/add_gloss_form.html', 
                                      {'add_gloss_form': form},
                                      context_instance=RequestContext(request))
        
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
            
            return update_definition(request, gloss, field, value)

        elif field == 'keywords':

            return update_keywords(gloss, field, value)
            
        elif field.startswith('relation'):
            
            return update_relation(gloss, field, value)
            
        elif field != 'regional_template' and field.startswith('region'):
            
            return update_region(gloss, field, value)
        
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
            
        
        elif field == 'inWeb':
            # only modify if we have publish permission
            if request.user.has_perm('dictionary.can_publish'):
                gloss.inWeb = (value == 'Yes')
                gloss.save() 
            
            if gloss.inWeb:
                newvalue = 'Yes'
            else:
                newvalue = 'No'
                
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
                if field == 'regional_template':
                    gloss.__setattr__(field, '')
                else:
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

def update_keywords(gloss, field, value):
    """Update the keyword field"""

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
    
    return HttpResponse(newvalue, {'content-type': 'text/plain'})

def update_region(gloss, field, value):
    """Update one of the regions for this gloss"""
    
    (what, regid) = field.split('_')
    
    try:
        region = Region.objects.get(id=regid)
    except:
        return HttpResponseBadRequest("Bad Region ID '%s'" % regid, {'content-type': 'text/plain'})

    if not gloss == region.gloss:
        return HttpResponseBadRequest("Region doesn't match gloss", {'content-type': 'text/plain'})
    
    if what == 'regiondelete':
        region.delete()
        return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id}) + "#regions")
    elif what == 'regiondialect':
        dialect = Dialect.objects.get(name=value)
        existing_region = gloss.region_set.filter(dialect=dialect)
        if len(existing_region) == 0 or existing_region[0] == region:
            region.dialect = dialect
            region.save()
        else:
            # We tried to change to an existing value, ignore it
            return HttpResponse(region.dialect.name, {'content-type': 'text/plain'})
    elif what == 'regionfrequency':
        region.frequency = value
        region.save()
    elif what == 'regiontraditional':
        if value == 1 or value == "1" or value == "traditional":
            region.traditional = True
            value = "traditional"
        else:
            region.traditional = False
            value = "attested"
        region.save()
        
    return HttpResponse(value, {'content-type': 'text/plain'})

def update_relation(gloss, field, value):
    """Update one of the relations for this gloss"""
    
    (what, relid) = field.split('_')

    try:
        rel = Relation.objects.get(id=relid)
    except:
        return HttpResponseBadRequest("Bad Relation ID '%s'" % defid, {'content-type': 'text/plain'})

    """if not rel.source == gloss:
        return HttpResponseBadRequest("Relation doesn't match gloss", {'content-type': 'text/plain'})
    """
    if what == 'relationdelete':
        print "DELETE: ", rel
        rel.delete()
        return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id}))
    elif what == 'relationroleforward':
        value, direction = value.split('_')
        if direction == 'backward':
            return HttpResponseBadRequest("Direction doesn't match", {'content-type': 'text/plain'})
        else:
            rel.role = Relationrole.objects.get(role=value)
            rel.save()
            newvalue = rel.role.forwardmessage
    elif what == 'relationrolebackward':
        value, direction = value.split('_')
        if direction == 'forward':
            return HttpResponseBadRequest("Direction doesn't match", {'content-type': 'text/plain'})
        else:
            rel.role = Relationrole.objects.get(role=value)
            rel.save()
            newvalue = rel.role.backwardmessage
    elif what == 'relationtarget':
        
        target = gloss_from_identifer(value)
        if target:
            rel.target = target
            rel.save()
            newvalue = str(target)
        else:
            return HttpResponseBadRequest("Badly formed gloss identifier '%s'" % value, {'content-type': 'text/plain'})
    else:
        
        return HttpResponseBadRequest("Unknown form field '%s'" % field, {'content-type': 'text/plain'})           
    
    return HttpResponse(newvalue, {'content-type': 'text/plain'})
            
def gloss_from_identifier(value):
    """Given an id of the form idgloss (pk) return the
    relevant gloss or None if none is found"""
    
    
    match = re.match('(.*) \((\d+)\)', value)
    if match:
        print "MATCH: ", match
        idgloss = match.group(1)
        pk = match.group(2)
        print "INFO: ", idgloss, pk
        
        target = Gloss.objects.get(pk=int(pk))
        print "TARGET: ", target
        return target
    else:
        return None
            
            

def update_definition(request, gloss, field, value):
    """Update one of the definition fields"""
    
    (what, defid) = field.split('_')
    try:
        defn = Definition.objects.get(id=defid)
    except:
        return HttpResponseBadRequest("Bad Definition ID '%s'" % defid, {'content-type': 'text/plain'})

    if not defn.gloss == gloss:
        return HttpResponseBadRequest("Definition doesn't match gloss", {'content-type': 'text/plain'})
    
    if what == 'definitiondelete':
        defn.delete()
        return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': gloss.id})+'?editdef')
    
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
        
        if request.user.has_perm('dictionary.can_publish'):
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


    return HttpResponse(newvalue, {'content-type': 'text/plain'})


def add_region(request, glossid):
    """Add a new region to a gloss"""

    if request.method == "POST":
        # Get the data, don't use a form it just adds overhead
        gloss = get_object_or_404(Gloss, id=glossid)
        dialect = get_object_or_404(Dialect, id=request.POST['dialect'])
        frequency = request.POST['frequency']
        if 'traditional' in request.POST and request.POST['traditional'] == "1":
            traditional = True
        else:
            traditional = False
        
        # Make sure there isn't already a dialect of this type
        if gloss.dialect.filter(name=dialect.name):
            return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': glossid})+'?editrel&error=DialectExists#regions')
        
        region = Region(gloss=gloss, dialect=dialect, frequency=frequency, traditional=traditional)
        region.save()
        
        return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': glossid})+'?editrel#regions')

def add_relation(request):
    """Add a new relation instance"""
    
    if request.method == "POST":
        
        form = RelationForm(request.POST)
        if form.is_valid():
            
            role = form.cleaned_data['role']
            role, direction = role.split('_')
            sourceid = form.cleaned_data['sourceid']
            targetid = form.cleaned_data['targetid']
            
            try:
                source = Gloss.objects.get(pk=int(sourceid))
            except:
                return HttpResponseBadRequest("Source gloss not found.", {'content-type': 'text/plain'})
            
            target = gloss_from_identifier(targetid)
            if target:
                if direction == 'backward':
                    rel = Relation(source=target, target=source, role=Relationrole.objects.get(role=role))
                    rel.save()
                else:
                    rel = Relation(source=source, target=target, role=Relationrole.objects.get(role=role))
                    rel.save()
                
                return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': source.id})+'?editrel#relations')
            else:
                return HttpResponseBadRequest("Target gloss not found.", {'content-type': 'text/plain'})
        else:
            print form

    # fallback to redirecting to the requesting page
    return HttpResponseRedirect('/')


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
            
    return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': thisgloss.id})+'?editdef')

@permission_required('dictionary.change_gloss')
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
                ti = get_object_or_404(TaggedItem, object_id=thisgloss.id, tag__name=tag)
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
        else:
            print "invalid form"
            print form.as_table()
            
    return response





