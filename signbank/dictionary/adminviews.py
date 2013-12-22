from django.views.generic.list import ListView

from signbank.dictionary.models import *
from signbank.dictionary.forms import *
from signbank.feedback.models import *


class GlossListView(ListView):
    
    model = Gloss
    template_name = 'dictionary/admin_gloss_list.html'
    paginate_by = 10
