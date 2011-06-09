# based on a django snippet from
# Author: wgollino (wgollino@yahoo.com)
# File: rangevaluesfilterspec.py


from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.contrib.admin.filterspecs import FilterSpec, BooleanFieldFilterSpec

class SenseNumberFilterSpec(FilterSpec):
    """
    Adds custom filter for sense number in the admin view
    
    need to set the property list_filter_sense = True on the field
    
    """

    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(SenseNumberFilterSpec, self).__init__(f, request, params, model, model_admin, field_path)
        self.field_generic = 'sense__'
        self.parsed_params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])

        self.links = [(_('All'), {}),
                      (_('No Senses'), {u'sense__isnull': True}),
                      (_('More than one'),{u'sense__gte': 1})]


    def choices(self, cl):
        for title, param_dict in self.links: 
            yield {'selected': self.parsed_params.keys() == param_dict.keys(),
                   'query_string': cl.get_query_string(param_dict, self.parsed_params),
                   'display': title}

# register the filter before the default filter
FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'list_filter_sense'), SenseNumberFilterSpec))


class DialectFilterSpec(BooleanFieldFilterSpec):
    """Custom filter for signbank that combines the Dialect fields into
    a single filter. Should be used just once on one of the fields.
    To use, set the property list_filter_dialect = True
    """

    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(DialectFilterSpec, self).__init__(f, request, params, model, model_admin, field_path)
        
        self.params = params
        
        self.filterfields =  [
                      (_("Australia Wide"), 'auslextf__exact'),
                      (_('Regional'), 'reglextf__exact'),
                      (_('NSW'), 'nswtf__exact'),
                      (_('TAS'), 'tastf__exact'),
                      (_('VIC'), 'victf__exact'),
                      (_('WA'),  'watf__exact'),
                      (_('SA'),  'satf__exact'),
                      (_('QLD'), 'qldtf__exact'),
                      (_('South'), 'sthtf__exact'),
                      ]
        terms = [t[1] for t in self.filterfields]
        self.ourparams = filter(lambda p: p in terms, params.keys())
        
        
    def title(self):
        return "Dialect"

#('auslextf', 'reglextf', 'nthtf', 'tastf', 'victf',  'watf', 'satf', 'qldtf', 'nswtf', 'sthtf', 
  # 'stateschtf', )

    def choices(self, cl):
        """cl is a Changelist"""
        
        yield {'selected': self.ourparams == [],
               'query_string': cl.get_query_string({}, self.ourparams),
               'display': 'All'}
        
        for title, fieldtest in self.filterfields:
            yield {'selected': self.params.has_key(fieldtest),
                   'query_string': cl.get_query_string({fieldtest: True}, self.ourparams),
                   'display': title}

# register the filter before the default filter
FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'list_filter_dialect'), DialectFilterSpec))


