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
        
        # validate
        # field is a valid field
        # value is a valid value for field
        
        
        if field.startswith('definition'):
            
            (what, defid) = field.split('_')
            try:
                defn = Definition.objects.get(id=defid)
            except:
                return HttpResponseBadRequest("Bad Definition ID '%s'" % defid, {'content-type': 'text/plain'})
        
            if not defn.gloss == gloss:
                return HttpResponseBadRequest("Definition doesn't match gloss", {'content-type': 'text/plain'})
            
            if what == 'definition':
                # update the definition
                defn.text = value
                defn.save()
                newvalue = defn.text
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
            
        else:
            

            if not field in Gloss._meta.get_all_field_names():
                return HttpResponseBadRequest("Unknown field", {'content-type': 'text/plain'})
            
            # special cases 
            # - Foreign Key fields (Language, Dialect)
            # - keywords
            # - videos
            # - tags
            
            gloss.__setattr__(field, value)
            gloss.save()
            
            
            f = Gloss._meta.get_field(field)
            newvalue = dict(f.flatchoices).get(value, value)
        
        return HttpResponse(newvalue, {'content-type': 'text/plain'})


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



def update_video(request, glossid):
    """View to update the video for a gloss from the form displayed on the staff view"""

    if not request.user.has_perm('dictionary.update_video'):
        return HttpResponseForbidden("Video Upload Not Allowed")


    keyword = None
    n = None
    videofile = None
    status = "form"

    thisgloss = get_object_or_404(Gloss, id=glossid)

    if request.method == "POST":
        form = VideoUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.has_key('videofile'):
                video = form.cleaned_data['videofile']
                # copy to comment video location
                basename = os.path.split(video.name)[-1]
                # this will be the path to the video, relative to MEDIA_ROOT
                videofile = os.path.join(settings.VIDEO_UPLOAD_LOCATION, basename)
                # make sure the target directory is there
                targetdir = os.path.join(settings.MEDIA_ROOT, settings.VIDEO_UPLOAD_LOCATION)
                if not os.path.exists(targetdir):
                    os.mkdir(targetdir)

                videoloc = os.path.join(settings.MEDIA_ROOT, videofile)
                video.rename(videoloc)

        elif request.POST.has_key("confirmvideofile"):
            # we're in the second stage confirmation
            videofile = request.POST['confirmvideofile']
            fullpath = os.path.join(settings.MEDIA_ROOT, videofile)

            if request.POST.has_key("Cancel"):
                if request.POST['Cancel'] == "cancel":
                    # remove the pending video file
                    if os.access(fullpath, os.F_OK):
                        os.unlink(fullpath)
                    status = "cancelled"
            else:
                # copy video to proper location
                newlocation = os.path.join(settings.MEDIA_ROOT, thisgloss.get_video_save_location())
                # backup existing file if any
                if os.access(newlocation, os.F_OK):
                    backup = newlocation + ".bak"
                    if os.access(backup, os.F_OK):
                        os.unlink(backup)
                    shutil.copy(newlocation, backup)


                # need to make sure the target directory is there
                try:
                    os.makedirs(os.path.dirname(newlocation))
                except:
                    pass

                # need shutil.copy here since we might be on different devices
                shutil.copy(fullpath, newlocation)
                os.unlink(fullpath)
                #os.rename(fullpath, newlocation)
                debug("Replaced video file: %s" % newlocation)
                status = "completed"
    else:
        form = VideoUpdateForm()

    return render_to_response("dictionary/update_video.html",
                              {'form': form,
                               'gloss' : thisgloss,
                               'keyword': keyword,
                               'n': n,
                               'videofile': videofile,
                               'status': status,
                               },
                              context_instance=RequestContext(request))


