from django.contrib import admin 
from signbank.dictionary.models import *
from reversion.admin import VersionAdmin


class KeywordAdmin(VersionAdmin):
    search_fields = ['^text']
    
    
class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 1
    raw_id_fields = ['translation']
    
    
class DefinitionInline(admin.TabularInline):
    model = Definition  
    extra = 1
    
class RelationInline(admin.TabularInline):
    model = Relation
    fk_name = 'source' 
    raw_id_fields = ['source', 'target']
    verbose_name_plural = "Relations to other Glosses"
    extra = 1

class GlossAdmin(VersionAdmin):
    fieldsets = ((None, {'fields': ('idgloss', 'annotation_idgloss', 'morph', 'sense', 
                                    'sn', 'StemSN', 'comptf', 'compound', 'language', 'dialect' )}, ),
              ('Publication Status', {'fields': ('inWeb', 'InMedLex', 
                                                 'isNew',  ), 
                                       'classes': ('collapse',)}, ),
              ('Lexis & Register: Borrowing', {'fields': ('aslgloss', 'asloantf', 'asltf', 
                                                           'bslgloss', 'bslloantf', ), 'classes': ('collapse',)}, ), 
              ('Lexis & Register: Religion', {'fields': ('religiontf', 'catholictf', 'cathschtf', 
                                                         'angcongtf', 'jwtf', 'otherreltf', ), 'classes': ('collapse',)}, ), 
              ('Lexis & Register: Iconicity', {'fields': ('transptf', 'transltf', 'obscuretf', 'opaquetf', ), 
                                             'classes': ('collapse',)}, ), 
              ('Lexis & Register: Other', {'fields': ('marginaltf', 'obsoletetf', 'varlextf', 
                                                      'doubtlextf', 'propernametf', 'fingersptf', 'gensigntf', 
                                                       'blendtf', 'blend', 'inittf', 'inittext', 
                                                      'restricttf', 'techtf', 'crudetf', 'setf',
                                                      'segloss', 'seonlytf', 'sedefinetf',), 'classes': ('collapse',)}, ), 
              ('Phonology', {'fields': ('handedness', 'onehand', 'doublehnd', 'twohand', 'domonly', 
                                        'Palm_orientation', 'alternate', 'sym', 'para', 'domhndsh', 
                                        'subhndsh', 'locprim', 'locsecond', ), 'classes': ('collapse',)}, ), 
              ('Morpho-Syntax', {'fields': ('dirtf', 'begindirtf', 'enddirtf', 
                                            'orienttf', 'bodyloctf', 'locdirtf', ), 'classes': ('collapse',)}, ), 
              ('Semantic Domains', {'fields': ('animalstf', 'arithmetictf', 'artstf', 'bodyprtstf', 
                                               'carstf', 'citiestf', 'clothingtf', 'colorstf', 
                                               'cookingtf', 'daystf', 'deaftf', 'drinkstf', 'eductf', 
                                               'familytf', 'feeltf', 'foodstf', 'furntf', 'govtf', 
                                               'groomtf', 'healthtf', 'judgetf', 'langactstf', 'lawtf', 
                                               'materialstf', 'metalgtf', 'mindtf', 'moneytf', 'naturetf', 
                                               'numbertf', 'ordertf', 'peopletf', 'physicalactstf', 'qualitytf', 
                                               'quantitytf', 'questsigntf', 'recreationtf', 'roomstf', 'saluttf', 
                                               'sensestf', 'sextf', 'shapestf', 'shoppingtf', 'sporttf', 
                                               'telecomtf', 'timetf', 'traveltf', 'utensilstf', 
                                               'weathertf', 'worktf', ), 'classes': ('collapse',)}, ), 
              ('Other', {'fields': ('queries', 'SpecialCore', 'tjspeculate', ), 'classes': ('collapse',)}, ),
              ('Obsolete Fields', {'fields': ('InMainBook', 'InSuppBook', 'NotBkDBOnly', 'inCD', 'BookProb','comp', ), 'classes': ('collapse',)}),
              )
    save_on_top = True
    save_as = True
    list_display = ['idgloss', 'annotation_idgloss', 'morph', 'sense', 'sn']
    search_fields = ['^idgloss', '=sn', '^annotation_idgloss']
    list_filter = ['language', 'dialect', 'sense', 'InMedLex', 'healthtf', 'inWeb', 'domhndsh']
    inlines = [ RelationInline, DefinitionInline, TranslationInline ]


class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'activation_key_expired', )
    search_fields = ('user__username', 'user__first_name', )
 
class DialectInline(admin.TabularInline):
    
    model = Dialect

class DialectAdmin(VersionAdmin):
    model = Dialect
 
class LanguageAdmin(VersionAdmin):
    model = Language
    inlines = [DialectInline]
    
admin.site.register(Dialect, DialectAdmin)
admin.site.register(Language, LanguageAdmin) 
admin.site.register(Gloss, GlossAdmin) 
admin.site.register(Keyword, KeywordAdmin) 

