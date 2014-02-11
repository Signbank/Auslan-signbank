from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.http import HttpResponse
import csv

from signbank.dictionary.models import *
from signbank.dictionary.forms import *
from signbank.feedback.models import *
from signbank.video.forms import VideoUploadForGlossForm
from tagging.models import Tag, TaggedItem

class GlossListView(ListView):
    
    model = Gloss
    template_name = 'dictionary/admin_gloss_list.html'
    paginate_by = 10
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GlossListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['searchform'] = GlossSearchForm(self.request.GET)
        context['glosscount'] = Gloss.objects.all().count()
        return context
    
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'CSV':
            return self.render_to_csv_response(context)
        else:
            return super(GlossListView, self).render_to_response(context)
    

    def render_to_csv_response(self, context):
        
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename="dictionary-export.csv"'
    
    
        fields = ['sn', 'idgloss', 'annotation_idgloss', 'morph']
    
        writer = csv.writer(response)
        header = [Gloss._meta.get_field(f).verbose_name for f in fields]
        header.append("Keywords")
        writer.writerow(header)
    
        for gloss in self.get_queryset():
            row = []
            for f in fields:
                row.append(getattr(gloss, f))
    
            trans = [t.translation.text for t in gloss.translation_set.all()]
            row.append(", ".join(trans))
    
            writer.writerow(row)
    
        return response

        
    def get_queryset(self):
        
        # get query terms from self.request
        qs = Gloss.objects.all()
        
        #print "QS:", len(qs)
        
        get = self.request.GET
        
        if get.has_key('search'):
            val = get['search']
            query = Q(idgloss__istartswith=val) | \
                    Q(annotation_idgloss__startswith=val) | \
                    Q(sn__startswith=val)
            qs = qs.filter(query)
            
            #print "A: ", len(qs)
            
            
        if get.has_key('keyword'):
            val = get['keyword']
            qs = qs.filter(translation__translation__text__startswith=val)
            
          
        if get.has_key('inWeb') and get['inWeb'] != '1':
            val = get['inWeb'] == '2'
            qs = qs.filter(inWeb__exact=val)
            #print "B :", len(qs)
                 
        ## phonology field filters
        if get.has_key('domhndsh') and get['domhndsh'] != '':
            val = get['domhndsh']
            qs = qs.filter(domhndsh__exact=val)
            
            #print "C :", len(qs)
            
        if get.has_key('subhndsh') and get['subhndsh'] != '':
            val = get['subhndsh']
            qs = qs.filter(subhndsh__exact=val)
            #print "D :", len(qs)
            
        if get.has_key('final_domhndsh') and get['final_domhndsh'] != '':
            val = get['final_domhndsh']
            qs = qs.filter(final_domhndsh__exact=val)
            #print "E :", len(qs)
            
        if get.has_key('final_subhndsh') and get['final_subhndsh'] != '':
            val = get['final_subhndsh']
            qs = qs.filter(final_subhndsh__exact=val)  
           # print "F :", len(qs)   
            
        if get.has_key('locprim') and get['locprim'] != '':
            val = get['locprim']
            qs = qs.filter(locprim__exact=val)
            #print "G :", len(qs)

        if get.has_key('locsecond') and get['locsecond'] != '':
            val = get['locsecond']
            qs = qs.filter(locsecond__exact=val)
            
            print "H :", len(qs)     

        if get.has_key('final_loc') and get['final_loc'] != '':
            val = get['final_loc']
            qs = qs.filter(final_loc__exact=val)   
            
            
        if get.has_key('initial_relative_orientation') and get['initial_relative_orientation'] != '':
            val = get['initial_relative_orientation']
            qs = qs.filter(initial_relative_orientation__exact=val)               

        if get.has_key('final_relative_orientation') and get['final_relative_orientation'] != '':
            val = get['final_relative_orientation']
            qs = qs.filter(final_relative_orientation__exact=val)   

        if get.has_key('initial_palm_orientation') and get['initial_palm_orientation'] != '':
            val = get['initial_palm_orientation']
            qs = qs.filter(initial_palm_orientation__exact=val)               

        if get.has_key('final_palm_orientation') and get['final_palm_orientation'] != '':
            val = get['final_palm_orientation']
            qs = qs.filter(final_palm_orientation__exact=val)  

        if get.has_key('initial_secondary_loc') and get['initial_secondary_loc'] != '':
            val = get['initial_secondary_loc']
            qs = qs.filter(initial_secondary_loc__exact=val)  

        if get.has_key('final_secondary_loc') and get['final_secondary_loc'] != '':
            val = get['final_secondary_loc']
            qs = qs.filter(final_secondary_loc__exact=val) 
            
           # print "G :", len(qs)
        # end of phonology filters
        
        
        vals = get.getlist('dialect', [])
        if vals != []:
            qs = qs.filter(dialect__in=vals)
            
           # print "H :", len(qs)
         
        vals = get.getlist('language', [])
        if vals != []:
            qs = qs.filter(language__in=vals)
            
            #print "I :", len(qs)
                     
        if get.has_key('tags') and get['tags'] != '':
            vals = get.getlist('tags')
            
            tags = [Tag.objects.get(pk=t) for t in vals]
 
            # search is an implicit AND so intersection
            tqs = TaggedItem.objects.get_intersection_by_model(Gloss, tags)
            
            # intersection
            qs = qs & tqs
            
          #  print "J :", len(qs)
            
        qs = qs.distinct()
        
        if get.has_key('nottags') and get['nottags'] != '':
            vals = get.getlist('nottags')
            
           # print "NOT TAGS: ", vals
            
            tags = [Tag.objects.get(pk=t) for t in vals]
 
            # search is an implicit AND so intersection
            tqs = TaggedItem.objects.get_intersection_by_model(Gloss, tags)
            
           # print "NOT", tags, len(tqs)
            # exclude all of tqs from qs
            qs = [q for q in qs if q not in tqs]   
            
           # print "K :", len(qs)
            
        
       # print "Final :", len(qs)
        return qs




class GlossDetailView(DetailView):
    
    model = Gloss
    context_object_name = 'gloss'
    
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GlossDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tagform'] = TagUpdateForm()
        context['videoform'] = VideoUploadForGlossForm()
        context['definitionform'] = DefinitionForm()
        context['navigation'] = context['gloss'].navigation(True)
        context['SIGN_NAVIGATION']  = settings.SIGN_NAVIGATION
        return context
        
    
