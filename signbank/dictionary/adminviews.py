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
        
        get = self.request.GET
        
        if get.has_key('search'):
            val = get['search']
            query = Q(idgloss__istartswith=val) | \
                    Q(annotation_idgloss__startswith=val) | \
                    Q(sn__startswith=val)
            qs = qs.filter(query)
          
        if get.has_key('inWeb') and get['inWeb'] != '1':
            val = get['inWeb'] == '2'
            qs = qs.filter(inWeb__exact=val)
                     
        if get.has_key('InMedLex') and get['InMedLex'] != '1':
            val = get['InMedLex'] == '2'
            qs = qs.filter(InMedLex__exact=val)
                 
        if get.has_key('domhndsh') and get['domhndsh'] != '':
            val = get['domhndsh']
            qs = qs.filter(domhndsh__exact=val)
             
        vals = get.getlist('dialect', [])
        if vals != []:
            qs = qs.filter(dialect__in=vals)
         
        vals = get.getlist('language', [])
        if vals != []:
            qs = qs.filter(language__in=vals)
                     
        if get.has_key('tags'):
            vals = get['tags']
            
            # get tags starting with the search string
            tags = Tag.objects.filter(name__istartswith=vals)
            tqs = TaggedItem.objects.get_union_by_model(Gloss, tags)
            
            # intersection
            qs = qs & tqs
            
        return qs




class GlossDetailView(DetailView):
    
    model = Gloss
    context_object_name = 'gloss'
    
