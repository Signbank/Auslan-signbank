"""Ingest data from a CSV file dumped from filemaker"""

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError  
from signbank.dictionary.models import *
import codecs
from unicodecsv import DictReader
import re
from tagging.models import Tag, TaggedItem

def c(s):
    """Return a cleand version of string s"""

    return s.encode('ascii', 'replace')



def cd(s):
    """Clean definition
    
    Remove number from start of definition (1. foo -> foo)
    """
    prefixes = ("Popular explanation: ", "Note: ")
    pat = r'(\d+\.)(.*)'
    
    m = re.match(pat, s)
    if m != None:
        gr = m.groups()
        return c(gr[1].strip())
    
    for prefix in prefixes:
        if s.startswith(prefix):
            return c(s.replace(prefix, ""))
    
    return c(s)
    
    

class Command(BaseCommand):
     
    help = 'ingest data from a CSV file dumped from Filemaker Pro'
    args = 'csvfile'

    tag_fields = {'religiontf': 'religion:religion',
                  'catholictf': 'religion:catholic', 
                  'cathschtf':  'religion:catholic school', 
                  'angcongtf':  'religion:anglican', 
                  'jwtf':       'religion:jehovas witness', 
                  'otherreltf': 'religion:other', 
                  'crudetf': 'lexis:crude', 
                  'daystf': 'semantic:day',
                  'deaftf': 'semantic:deaf',
                  'alternate': 'phonology:alternating', 
                  'animalstf': 'semantic:animal',
                  'arithmetictf': 'semantic:arithmetic',
                  'artstf': 'semantic:arts',
                  'bodyloctf': 'morph:body locating',
                  'bodyprtstf': 'semantic:bodypart',
                  'carstf': 'semantic:car',
                  'citiestf': 'semantic:city',
                  'clothingtf': 'semantic:clothing',
                  'colorstf': 'semantic:color',
                  'cookingtf': 'semantic:cooking',
                  'dirtf': 'morph:directional sign',
                  'begindirtf': 'morph:begin directional sign',
                  'enddirtf': 'morph:end directional sign',
                  'doublehnd': 'phonology:double handed',
                  'domonly': 'phonology:dominant hand only',
                  'twohand': 'phonology:two handed',
                  'doubtlextf': 'lexis:doubtlex',
                  'drinkstf': 'semantic:drink',
                  'eductf': 'semantic:education',
                  'familytf': 'semantic:family',
                  'feeltf': 'semantic:feel',
                  'fingersptf': 'lexis:fingerspell',
                  'foodstf': 'semantic:food',
                  'furntf': 'semantic:furniture',
                  'gensigntf': 'lexis:gensign',
                  'govtf': 'semantic:government',
                  'groomtf': 'semantic:groom', 
                  'healthtf': 'semantic:health',
                  'judgetf': 'semantic:judge',
                  'langactstf': 'semantic:language act',
                  'lawtf': 'semantic:law',
                  'locdirtf': 'morph:locational and directional',
                  'marginaltf': 'lexis:marginal',
                  'materialstf': 'semantic:material',
                  'metalgtf': 'semantic:metalg',
                  'mindtf': 'semantic:mind',
                  'moneytf': 'semantic:money',
                  'naturetf': 'semantic:nature',
                  'numbertf': 'semantic:number',
                  'obscuretf': 'iconicity:obscure',
                  'obsoletetf': 'lexis:obsolete',
                  'onehand': 'phonology:onehand',
                  'opaquetf': 'iconicity:opaque',
                  'ordertf': 'semantic:order',
                  'orienttf': 'morph:orientating sign',
                  'para': 'phonology:parallel',
                  'peopletf': 'semantic:people',
                  'physicalactstf': 'semantic:physical act',
                  'propernametf': 'lexis:proper name',
                  'qualitytf': 'semantic:quality',
                  'quantitytf': 'semantic:quantity',
                  'para': 'phonology:parallel',
                  'questsigntf': 'semantic:question',
                  'recreationtf': 'semantic:recreation',
                  'reglextf': 'lexis:regional',
                  'restricttf': 'lexis:restricted lexeme',
                  'roomstf': 'semantic:rooms',
                  'saluttf': 'semantic:salutation',
                  'sensestf': 'semantic:sensing',
                  'seonlytf': 'lexis:signed english only',
                  'setf': 'lexis:signed english',
                  'sextf': 'semantic:sexuality',
                  'shapestf': 'semantic:shapes',
                  'shoppingtf': 'semantic:shopping',
                  'sporttf': 'semantic:sport',
                  'stateschtf': 'school:state school',
                  'sym': 'phonology:symmetrical',
                  'techtf': 'lexis:technical',
                  'telecomtf': 'semantic:telecommunications',
                  'timetf': 'semantic:time',
                  'transltf': 'iconicity:translucent',
                  'transptf': 'iconicity:transparent',
                  'traveltf': 'semantic:travel',
                  'utensilstf': 'semantic:utensil',
                  'varlextf': 'lexis:varlex',
                  'weathertf': 'semantic:weather',
                  'worktf': 'semantic:work',
                  
                  'Attested in Corpus': 'corpus:attested',
                  'Forearm rotation': 'phonology:forearm rotation',
                  'hschange': 'phonology:handshape change',
                  'Battinson': 'lexis:battinson',
                  'Classifier/Constructed Action': 'lexis:classifier',
                  'B92 reg': 'b92:regional',
                  'B92 dir': 'b92:directional',
                   }



    def handle(self, *args, **options):
        
        # drop all glosses
        Gloss.objects.all().delete()
        TaggedItem.objects.all().delete()
        Translation.objects.all().delete()
        Keyword.objects.all().delete()
        
        
        (lang_bsl, created) = Language.objects.get_or_create(name='BSL')
        for csvfile in args:
            
            #h = csv.DictReader(codecs.open(csvfile, 'Ur', encoding='iso8859-1'))
            h = DictReader(open(csvfile, 'U'), encoding='iso8859-1')
            
            for row in h:
                #if row['annotation idgloss'].startswith('B'):
                #    break
                
                if row['bsltf'] == 'T':
                    
                    for key in row.keys():
                        row[key] = row[key].strip()
                    
                    print row['annotation idgloss'], row['sn'], row['idgloss']
                    gloss = Gloss()
                    gloss.annotation_idgloss = row['annotation idgloss']
                    gloss.bsltf = True
                    gloss.inWeb = False
                    gloss.asltf = row['asltf']
                    
                    if row['sn'] != '':
                        gloss.sn = int(row['sn'])
                        
                    if row['idgloss'] != '':
                        gloss.idgloss = row['idgloss']
                    else:
                        gloss.idgloss = gloss.annotation_idgloss
                    
                    if row['domhndsh'] != '':
                        gloss.domhndsh = row['domhndsh']
                    if row['subhndsh'] != '':
                        gloss.subhndsh = row['subhndsh']
                    if row['FinaldominantHS'] != '':
                        gloss.final_domhndsh = row['FinaldominantHS']
                    if row['FinalSubordinateHS'] != '':
                        gloss.final_subhndsh = row['FinalSubordinateHS']
                    if row['FinalLoc'] != '':
                        gloss.final_loc = row['FinalLoc']
                    if row['locprim'] != '':
                        gloss.locprim = int(row['locprim'])
                    if row['locsecond'] != '':
                        gloss.locsecond = int(row['locsecond'])
                    
                    
                    if row['PalmOriInitial'] != '':
                        gloss.initial_palm_orientation = row['PalmOriInitial']
                    if row['PalmOriFinal'] != '':
                        gloss.final_palm_orientation = row['PalmOriFinal']
                    
                    
                    if row['prim2ndloc'] != '':
                        gloss.initial_secondary_loc = row['prim2ndloc']
                    if row['fin2ndloc'] != '':
                        gloss.final_secondary_loc = row['fin2ndloc']
                        
                    if row['Initrelori'] != '':
                        gloss.initial_relative_orientation = row['Initrelori']
                    if row['Finrelori'] != '':
                        gloss.final_relative_orientation = row['Finrelori']                       
                        
                        

                    gloss.morph = row['morph']
                    if row['sense'] != '':
                        gloss.sense = int(row['sense'])
                        
                    gloss.comptf = row['comptf'] == 'T'
                    gloss.compound = row['compound']
                    
                    gloss.segloss = row['segloss']
                    
                    # save direct properties
                    gloss.save()
                    
                    # definitions 
                    
                    count = 1
                    for field in ['interact1', 'interact2', 'interact3']:
                        if row[field] != '':
                            dfn = Definition(gloss=gloss, text=cd(row[field]), role='interact', count=count)
                            #print "INTERACT: ", count, row[field]
                            count += 1
                            dfn.save()
                    
                    count = 1
                    for field in ['modifier1', 'modifier2', 'modifier3']:
                        if row[field] != '':
                            dfn = Definition(gloss=gloss, text=cd(row[field]), role='modifier', count=count)
                            #print "Modifier: ", count, row[field]
                            count += 1
                            dfn.save()                   

                    count = 1
                    for field in ['nom1', 'nom2', 'nom3', 'nom4', 'nom5']:
                        if row[field] != '':
                            dfn = Definition(gloss=gloss, text=cd(row[field]), role='noun', count=count)
                            #print "Noun: ", count, row[field]
                            count += 1
                            dfn.save()  
                    
                    if row['PopExplain'] != '':
                        dfn = Definition(gloss=gloss, text=cd(row['PopExplain']), role='popexplain', count=1)
                        #print "Popular Explanation: ", count, row['PopExplain']
                        dfn.save()
                        
                    if row['tjspeculate'] != '':
                        dfn = Definition(gloss=gloss, text=cd(row['tjspeculate']), role='privatenote', count=1)
                        #print "TJSpeculate (Private Note): ", count, row['tjspeculate']
                        dfn.save()                    
                        
                    if row['queries'] != '':
                        dfn = Definition(gloss=gloss, text=cd(row['queries']), role='privatenote', count=1)
                        #print "Query (Private Note): ", count, row['queries']
                        dfn.save()
                        
                    count = 1
                    for field in ['question1', 'question2']:
                        if row[field] != '':
                            dfn = Definition(gloss=gloss, text=cd(row[field]), role='question', count=count)
                            #print "Question: ", count, row[field]
                            count += 1
                            dfn.save()     

                    if row['CorrectionsAdditionsComments'] != '':
                        dfn = Definition(gloss=gloss, text=cd(row['CorrectionsAdditionsComments']), role='privatenote', count=1)
                        dfn.save()                            
                            
                        
                    count = 1
                    for field in ['verb1', 'verb2', 'verb3', 'verb4', 'verb5']:
                        if row[field] != '':
                            dfn = Definition(gloss=gloss, text=cd(row[field]), role='verb', count=count)
                            #print "Verb: ", count, row[field]
                            count += 1
                            dfn.save()                      
                    
                    # keywords
                    kwds = row['Combined Keywords'].split(',')
                    kwds = [c(k.strip()) for k in kwds]
                    #print "|".join(kwds)
                    count = 1
                    for kwd in kwds:
                        if kwd != '':
                            (k, created) = Keyword.objects.get_or_create(text=c(kwd))
                            tr = Translation(gloss=gloss, translation=k, index=count)
                            count += 1
                            tr.save()
                    # tags
                    
                    for field in self.tag_fields.keys():
                        if row[field] == 'T':
                     #       print '\t', self.tag_fields[field]
                            Tag.objects.add_tag(gloss, '"%s"' %  self.tag_fields[field])
                    #print ""
                    
                    # special case tags/definitions
                    
                    if row['B92 rel'] != '':
                        if row['B92 rel'] == 'phvar':
                            Tag.objects.add_tag(gloss, 'B92:variant')
                            Tag.objects.add_tag(gloss, 'B92:present')
                        elif row['B92 rel'] == 'phsame':
                            Tag.objects.add_tag(gloss, 'B92:present')
                    
                    if row['B92 sn'] != '':
                        dfn = Definition(gloss=gloss, text=row['B92 sn'], role='B92 sn', count=1)
                        dfn.save()
                    
                    gloss.language.add(lang_bsl)
                    
                    gloss.save()
                    
                    
            # relations need to wait until we've made all glosses
            print "Ingesting relations..."
            
            Relation.objects.all().delete()

            #h = csv.DictReader(codecs.open(csvfile, 'Ur', encoding='iso8859-1'))
            h = DictReader(open(csvfile, 'U'), encoding='iso8859-1')
            for row in h:                    

                #if row['annotation idgloss'].startswith('B'):
                #    break
                
                if row['bsltf'] and row['idgloss'] != '':
                    try:
                        
                        thisgloss = Gloss.objects.get(idgloss__exact=row['idgloss'])
                    except:
                        print "Can't find gloss for ", row['idgloss']
                        continue
                    
                    # syn
                    # var
                    generate_relations(thisgloss, row, ['varb', 'varc', 'vard', 'vare'], 'variant')
                    generate_relations(thisgloss, row, ['syn1', 'syn2', 'syn3'], 'synonym')
                    
                    
                    
                    
def generate_relations(thisgloss, row, relfields, role):  
                     
    for field in relfields:
        if row[field] != '':                           
            try:
                target = Gloss.objects.get(idgloss__exact=row[field])
            
                rel = Relation(source=thisgloss, target=target, role=role)
                rel.save()
                                            
                print thisgloss, "-(%s)->" % role, target
            except:
                print "Can't find", role , row[field]
                    
                    
                    
                    