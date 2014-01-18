from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from signbank.dictionary.models import *
from signbank.dictionary.forms import *
from signbank.feedback.models import *
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
        return context
    

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
            vals = get['tags']
            
            #print "TAGS: ", vals
            # get tags starting with the search string
            tags = Tag.objects.filter(name__istartswith=vals)
            tqs = TaggedItem.objects.get_union_by_model(Gloss, tags)
            
            # intersection
            qs = qs & tqs
            
            
           # print "J :", len(qs)
            
        
       # print "Final :", len(qs)
        return qs




class GlossDetailView(DetailView):
    
    model = Gloss
    context_object_name = 'gloss'
    
