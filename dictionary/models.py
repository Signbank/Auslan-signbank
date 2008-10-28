"""Models for the Auslan database.

These are refactored from the original database to 
normalise the data and hopefully make it more
manageable.  

"""

from django.db import models
from models_legacy import Sign

handedness_choices = (("One", "One"),("Two", "Two"), ("Double", "Double"))

class Translation(models.Model):
    """An English translations of Auslan glosses"""
     
    gloss = models.ForeignKey("Gloss")
    translation = models.ForeignKey("Keyword")
    
    def __str__(self):
        return str(self.gloss)+"-"+str(self.translation)
    
    def get_absolute_url(self):
        """Return a URL for a view of this translation."""
        
        alltrans = self.translation.translation_set.all()
        idx = 0
        for tr in alltrans: 
            if tr == self:
                return "/dictionary/words/"+str(self.translation)+"-"+str(idx+1)+".html"
            idx += 1
        return "/dictionary/"
        
    
    class Meta:
        ordering = ['gloss']
        
    class Admin:
        list_display = ['gloss', 'translation']
        search_fields = ['gloss__idgloss']
    
    
    
class Keyword(models.Model):
    """An english keyword that will be a translation of a sign"""
    
    def __str__(self):
        return self.text
    
    text = models.CharField(max_length=50)
    
    def inWeb(self):
        """Return True if some gloss associated with this
        keyword is in the web version of the dictionary"""
        
        return len(self.translation_set.filter(gloss__inWeb__exact=True)) != 0
            
    class Meta:
        ordering = ['text']
        
    class Admin:
        search_fields = ['text']
    
    
defn_role_choices = (('noun', 'Noun'),
                     ('verb', 'Verb'), 
                     ('deictic', 'Deictic'),
                     ('interact', 'Interact'),
                     ('modifier', 'Modifier'),
                     ('question', 'Question'),
                     ('popexplain', 'Popular Explanation'),
                     ('augment', 'Augment'),
                     )


class Definition(models.Model):
    """An English text associated with an Auslan glosses"""
    
    def __str__(self):
        return str(self.gloss)+"/"+self.role
        
    gloss = models.ForeignKey("Gloss")
    text = models.TextField()
    role = models.CharField(max_length=20, choices=defn_role_choices)  
    count = models.IntegerField() 

    class Meta:
        ordering = ['gloss']
        
    class Admin:
        list_display = ['gloss', 'role', 'count', 'text']
        list_filter = ['role']
        search_fields = ['gloss__idgloss']
        
    
  
handshapeChoices = (('0.1', 'Round'),
                    ('0.2', 'Okay'),
                    ('1.1', 'Point'),
                    ('1.2', 'Hook'),
                    ('2.1', 'Two'),
                    ('2.2', 'Kneel'),
                    ('2.3', 'Perth'),
                    ('2.4', 'Spoon'),
                    ('2.5', 'Letter-n'),
                    ('2.6', 'Wish'),
                    ('3.1', 'Three'),
                    ('3.2', 'Mother'),
                    ('3.3', 'Letter-m'),
                    ('4.1', 'Four'),
                    ('5.1', 'Spread'),
                    ('5.2', 'Ball'),
                    ('5.3', 'Flat'),
                    ('5.4', 'Thick'),
                    ('5.5', 'Cup'),
                    ('6.1', 'Good'),
                    ('6.2', 'Bad'),
                    ('7.1', 'Gun'),
                    ('7.2', 'Letter-c'),
                    ('7.3', 'Small'),
                    ('7.4', 'Seven'),
                    ('8.1', 'Eight'),
                    ('9.1', 'Nine'), 
                    ('10.1', 'Fist'),
                    ('10.2', 'Soon'),
                    ('10.3', 'Ten'),
                    ('11.1', 'Write'),
                    ('12.1', 'Salt'),
                    ('13.1', 'Middle'),
                    ('14.1', 'Rude'),
                    ('15.1', 'Ambivalent'),
                    ('16.1', 'Love'),
                    ('17.1', 'Animal'),
                    ('18.1', 'Queer'),                     
                     )
                     
locationChoices = (
                    ('1', 'Top of head'),
                    ('2', 'Forehead'),
                    ('3', 'Temple'),
                    ('4', 'Eye'),
                    ('5', 'Nose'),
                    ('6', 'Whole of face'),
                    ('7', 'Cheekbone'),
                    ('8', 'Ear or side of head'),
                    ('9', 'Cheek'),
                    ('10', 'Mouth and lips'),
                    ('11', 'Chin'),
                    ('12', 'Neck'),
                    ('13', 'Shoulder'),
                    ('14', 'Chest or high neutral space'),
                    ('15', 'Stomach or middle neutral space'),
                    ('16', 'Waist or low neutral space'),
                    ('17', 'Below waist'),
                    ('18', 'Upper arm'),
                    ('19', 'Elbow'),
                    )
secLocationChoices = (
                    ('20', 'Pronated forearm'),
                    ('21', 'Supinated forearm'),
                    ('22', 'Pronated wrist'),
                    ('23', 'Spinated wrist'),
                    ('24', 'Back of hand'),
                    ('25', 'Palm'),
                    ('26', 'Edge of hand'),
                    ('27', 'Fingertips'),
                    )



    
class Gloss(models.Model):
    
    class Meta:
        verbose_name_plural = "Glosses"
        ordering = ['idgloss']
        permissions = (('update_video', "Can Update Video"), )

        
    def __str__(self):
        return str(self.id)+"-"+self.idgloss
    
    idgloss = models.CharField(max_length=50)    
  
    annotation_idgloss = models.CharField(blank=True, max_length=30) 
        # the idgloss used in transcription, may be shared between many signs

    
    alternate = models.BooleanField("Alternating", null=True, blank=True)
    angcongtf = models.BooleanField("Anglican", null=True, blank=True)
    animalstf = models.BooleanField(null=True, blank=True)

    
    arithmetictf = models.BooleanField(null=True, blank=True)
    artstf = models.BooleanField(null=True, blank=True)
    
    aslgloss = models.CharField("ASL gloss", blank=True, max_length=50) # American Sign Language gloss
    asloantf = models.BooleanField("ASL loan sign", null=True, blank=True)
    asltf = models.BooleanField("ASL sign", null=True, blank=True)
    
    auslextf = models.BooleanField("Auslan lexeme", null=True, blank=True)
    begindirtf = models.BooleanField("Begin directional sign", null=True, blank=True)
    
    blend = models.CharField("Blend of", max_length=100, null=True, blank=True) # This field type is a guess.
    blendtf = models.BooleanField("Blend", null=True, blank=True)
    
    bodyloctf = models.BooleanField("Body Locating sign", null=True, blank=True)
    bodyprtstf = models.BooleanField(null=True, blank=True)
    BookProb = models.BooleanField(null=True, blank=True)
    
    # loans from british sign language
    bslgloss = models.CharField("BSL gloss", max_length=50, blank=True) 
    bslloantf = models.BooleanField("BSL loan sign", null=True, blank=True)
    bsltf = models.BooleanField("BSL sign", null=True, blank=True)
    
    carstf = models.BooleanField(null=True, blank=True)
    catholictf = models.BooleanField("Catholic Sign", null=True, blank=True)
    cathschtf = models.BooleanField("Catholic School", null=True, blank=True) 
    
    citiestf = models.BooleanField(null=True, blank=True)
    clothingtf = models.BooleanField(null=True, blank=True)
    colorstf = models.BooleanField(null=True, blank=True)
    comp = models.BooleanField(null=True, blank=True) 
    compound = models.CharField("Compound of", max_length=100, blank=True) # This field type is a guess.
    comptf = models.BooleanField("Compound", null=True, blank=True)
    cookingtf = models.BooleanField(null=True, blank=True)
    CorrectionsAdditionsComments = models.TextField(null=True, blank=True) # This field type is a guess.
    crudetf = models.BooleanField(null=True, blank=True)
    daystf = models.BooleanField(null=True, blank=True)
    deaftf = models.BooleanField(null=True, blank=True)
    
    
    dirtf = models.BooleanField("Directional Sign", null=True, blank=True)
    
    
    handedness = models.CharField("Handedness", max_length=10, choices=handedness_choices, blank=True)  
    domhndsh = models.CharField("Dominant Hand Shape", blank=True, choices=handshapeChoices, max_length=5)  
    subhndsh = models.CharField("Subordinate Hand Shape", null=True, choices=handshapeChoices, blank=True, max_length=5) 
    domonly = models.BooleanField("Dominant hand only", null=True, blank=True) 
    twohand = models.BooleanField("Two handed", null=True, blank=True) 
    doublehnd = models.BooleanField("Double handed", null=True, blank=True) 
    
    locprim = models.IntegerField("Primary Location", choices=locationChoices, null=True, blank=True) 
    locsecond = models.IntegerField("Secondary Location", choices=secLocationChoices, null=True, blank=True) 
    
    
    doubtlextf = models.BooleanField(null=True, blank=True)
    drinkstf = models.BooleanField(null=True, blank=True)
    eductf = models.BooleanField(null=True, blank=True)
    enddirtf = models.BooleanField("End directional sign", null=True, blank=True)
       
    familytf = models.BooleanField(null=True, blank=True)
    feeltf = models.BooleanField(null=True, blank=True)
    fingersptf = models.BooleanField(null=True, blank=True)
    foodstf = models.BooleanField(null=True, blank=True)
    furntf = models.BooleanField(null=True, blank=True)
    general = models.TextField(null=True, blank=True)  
    gensigntf = models.BooleanField(null=True, blank=True)
    govtf = models.BooleanField(null=True, blank=True)
    groomtf = models.BooleanField(null=True, blank=True)
    

    healthtf = models.BooleanField(null=True, blank=True) 
    
    
    # which versions of the dictionary should this gloss appear in
    inCD = models.BooleanField("In the CDROM dictionary", null=True, blank=True) 
    inWeb = models.BooleanField("In the Web dictionary", default=False)
    InMainBook = models.BooleanField("In the main book", null=True, blank=True)
    InSuppBook = models.BooleanField("In the supplementary book", null=True, blank=True)  
    InMedLex = models.BooleanField("In Medical SignBank", null=True, default=False)  
    isNew = models.BooleanField("Is this a proposed new sign?", null=True, default=False)
    
    inittext = models.CharField(max_length="50", blank=True) 
    inittf = models.BooleanField(null=True, blank=True)

    
    judgetf = models.BooleanField(null=True, blank=True)
    jwtf = models.BooleanField("Jehova's Witness", null=True, blank=True)
    langactstf = models.BooleanField(null=True, blank=True)
    lawtf = models.BooleanField(null=True, blank=True)
    locdirtf = models.BooleanField("Locational and directional", null=True, blank=True)
    marginaltf = models.BooleanField(null=True, blank=True)
    materialstf = models.BooleanField(null=True, blank=True)
    metalgtf = models.BooleanField(null=True, blank=True) 
    mindtf = models.BooleanField(null=True, blank=True) 
    
    moneytf = models.BooleanField(null=True, blank=True)
    morph = models.CharField("Morphemic Analysis", max_length=50, blank=True)  
    
    naturetf = models.BooleanField(null=True, blank=True)
    
    NotBkDBOnly = models.BooleanField("Not in book, database only", null=True, blank=True) 
    numbertf = models.BooleanField(null=True, blank=True)
    obscuretf = models.BooleanField("Obscure", null=True, blank=True)
    obsoletetf = models.BooleanField(null=True, blank=True)
    onehand = models.BooleanField(null=True, blank=True)
    opaquetf = models.BooleanField("Opaque", null=True, blank=True)
    ordertf = models.BooleanField(null=True, blank=True)
    orienttf = models.BooleanField("Orientating sign", null=True, blank=True)
    otherreltf = models.BooleanField("Other Religion", null=True, blank=True)
    Palm_orientation = models.CharField(max_length=10, blank=True) # only used twice = Left
    para = models.BooleanField("Parallel", null=True, blank=True) 
    peopletf = models.BooleanField("People", null=True, blank=True)
    physicalactstf = models.BooleanField("Physical acts", null=True, blank=True)
    
    propernametf = models.BooleanField(null=True, blank=True)

    qualitytf = models.BooleanField("Qualities", null=True, blank=True)
    quantitytf = models.BooleanField("Quantities", null=True, blank=True)
    queries = models.TextField(null=True, blank=True) # This field type is a guess.
    
    questsigntf = models.BooleanField("Questions", null=True, blank=True)
    recreationtf = models.BooleanField("Recreation", null=True, blank=True)
    reglextf = models.BooleanField(null=True, blank=True)
    religiontf = models.BooleanField("Religious Sign", null=True, blank=True)
    restricttf = models.BooleanField("Restricted Lexeme", null=True, blank=True)
    roomstf = models.BooleanField("Rooms", null=True, blank=True)
    saluttf = models.BooleanField("Salutation", null=True, blank=True)
    sedefinetf = models.TextField("Signed English definition available", null=True, blank=True)
    segloss = models.CharField("Signed English gloss", max_length=50, blank=True) 
    sensestf = models.BooleanField("Sensing", null=True, blank=True)
    seonlytf = models.BooleanField("Signed English only sign", null=True, blank=True)
    setf = models.BooleanField("Signed English", null=True, blank=True)
    sextf = models.BooleanField("Sexuality", null=True, blank=True)
    shapestf = models.BooleanField("Shapes", null=True, blank=True)
    shoppingtf = models.BooleanField("Shopping", null=True, blank=True)
    SpecialCore = models.TextField(null=True, blank=True) # This field type is a guess.
    sporttf = models.BooleanField("Sport", null=True, blank=True)
    stateschtf = models.BooleanField("State School", null=True, blank=True)
    sthtf = models.BooleanField("Southern Dialect", null=True, blank=True)
    sym = models.BooleanField("Symetrical", null=True, blank=True) 
    
    
    techtf = models.BooleanField("Technical Lexeme", null=True, blank=True)
    telecomtf = models.BooleanField("Telecommunications", null=True, blank=True)
    timetf = models.BooleanField("Time", null=True, blank=True)
    tjspeculate = models.TextField(null=True, blank=True) # This field type is a guess.
    transltf = models.BooleanField("Translucent", null=True, blank=True)
    transptf = models.BooleanField("Transparent", null=True, blank=True)
    traveltf = models.BooleanField("Travel", null=True, blank=True)
    utensilstf = models.BooleanField("Utensils", null=True, blank=True)
    
    varlextf = models.BooleanField(null=True, blank=True)
    
    #
    # usage of the sign in various states
    #
    tastf = models.BooleanField("Tasmania", null=True, blank=True) # used in Tasmania    
    victf = models.BooleanField("Victoria", null=True, blank=True) # used in Victoria
    watf = models.BooleanField("Western Australia", null=True, blank=True)  # used in Western Australia
    satf = models.BooleanField("South Australia", null=True, blank=True)  # used in South Australia
    qldtf = models.BooleanField("QLD", null=True, blank=True) # used in Queensland 
    nswtf = models.BooleanField("NSW", null=True, blank=True) # used in NSW
    nthtf = models.BooleanField("Northern Dialect", null=True, blank=True) # used in Northern Territory
    
    weathertf = models.BooleanField(null=True, blank=True)
    worktf = models.BooleanField(null=True, blank=True)
    

    
    sense = models.IntegerField("Sense Number", null=True, blank=True) 
    sn = models.IntegerField("Sign Number", null=True, blank=True)   # this is a sign number - was trying
            # to be a primary key, also defines a sequence - need to keep the sequence
            # and allow gaps between numbers for inserting later signs
            
    
    
    StemSN = models.IntegerField(null=True, blank=True) 

    def next_dictionary_gloss(self):
        """Find the next gloss in dictionary order"""
        return Gloss.objects.filter(sn__gt=self.sn, inWeb__exact=True).order_by('sn')[0]
 
    
    def prev_dictionary_gloss(self):
        """Find the previous gloss in dictionary order"""
        return Gloss.objects.filter(sn__lt=self.sn, inWeb__exact=True).order_by('-sn')[0]
        

    def get_absolute_url(self):
        return "/dictionary/gloss/%s.html" % self.idgloss
    
    def get_video_url(self):
        """return  the url of the video for this gloss which may be that of a homophone"""
         
        # first set the default
        video_num = self.sn
        # then check if we need to change
        if self.sense > 1:
            homophones = self.relation_sources.filter(role='homophone', target__sense__exact=1)
            # should be only zero or one of these
            if len(homophones) > 0:   
                video_num = homophones[0].target.sn
                
        return "video/"+str(video_num)[:2]+"/"+str(video_num)+".flv"
    
    def definitions(self):
        """gather together the definitions for this gloss"""
    
        defs = dict()
        for d in self.definition_set.all().order_by('count'):
            if not defs.has_key(d.role):
                defs[d.role] = []
            
            defs[d.role].append(d.text)
        return defs
    
    class Admin:
        save_on_top = True
        search_fields = ['^idgloss']
    
        fields = (
            (None, {
                    'fields':  ( 'idgloss', 'annotation_idgloss', 'morph',  'sense', 'sn', 'StemSN')

                   }), 
                   
            ('Publication Status', { 
                    'classes': 'collapse',
                    'fields' : ('inCD', 'inWeb', 'InMainBook', 'InSuppBook', 'InMedLex', 'isNew', 'NotBkDBOnly', 'BookProb', )
                   }),
            ('Lexis & Register: Borrowing', { 
                   'fields': ('aslgloss', 'asloantf', 'asltf','bslgloss', 'bslloantf', 'bsltf'),
                   'classes': 'collapse',     
                   }),
            ('Lexis & Register: States', {
                    'classes': 'collapse',
                    'fields' : ( 'auslextf', 'reglextf', 'nthtf', 'tastf', 'victf', 'watf', 'satf', 'qldtf', 'nswtf','sthtf',  'stateschtf',)
                   }), 
            
            ('Lexis & Register: Religion', {
                    'classes': 'collapse',
                    'fields' : (  'religiontf', 'catholictf', 'cathschtf', 'angcongtf', 'jwtf', 'otherreltf', )
                   }),
            ('Lexis & Register: Iconicity', {
                    'classes': 'collapse',
                    'fields' : (   'setf', 'segloss', 'seonlytf', 'sedefinetf','transptf', 'transltf','obscuretf',  'opaquetf',)
                   }),               
            ('Lexis & Register: Other', {
                'classes': 'collapse',
                'fields' : ('marginaltf', 'obsoletetf', 'varlextf', 'doubtlextf', 'propernametf',
                            'fingersptf', 'gensigntf', 'comptf', 'compound', 'blendtf', 'blend',
                            'inittf', 'inittext',  'restricttf','techtf',  'crudetf', )
                }),               
            ('Phonology', {
                    'classes': 'collapse',
                    'fields' : ('handedness',  'onehand', 'doublehnd', 'twohand', 'domonly',
                                 'Palm_orientation','alternate', 'sym', 'para',
                                'domhndsh', 'subhndsh', 'locprim', 'locsecond')
                   }),                    
            ('Morpho-Syntax', {
                'classes': 'collapse',
                'fields' : ( 'dirtf', 'begindirtf', 'enddirtf', 'orienttf', 'bodyloctf', 'locdirtf',)
                }),
         
 
             ("Semantic Domains", {
                    'classes': 'collapse',
                    'fields':  ( 'animalstf', 'arithmetictf', 'artstf', 
                        'bodyprtstf', 'carstf',   'citiestf', 'clothingtf', 'colorstf',
                        'cookingtf','daystf', 'deaftf',  'drinkstf', 'eductf', 
                                 'familytf', 'feeltf',  'foodstf', 
                                'furntf',  'govtf', 'groomtf', 'healthtf',
                                'judgetf',  'langactstf', 'lawtf',
                                 'materialstf', 'metalgtf', 'mindtf', 'moneytf', 
                                'naturetf', 'numbertf', 
                                'ordertf',  
                                 'peopletf', 'physicalactstf',  'qualitytf', 'quantitytf',
                                 'questsigntf', 'recreationtf',  
                                'roomstf', 'saluttf', 
                                'sensestf',  'sextf', 'shapestf', 'shoppingtf','sporttf',
                                'telecomtf', 'timetf', 'traveltf',  'utensilstf',   'weathertf', 
                                'worktf',)

                   }),       
            
            ("Other", {
                    'classes': 'collapse',
                    'fields':  ( 'general',    
                                 'comp', 
                                 'CorrectionsAdditionsComments', 
                                'queries',  
                                'SpecialCore', 
                                 'tjspeculate',  
                                 )

                   }),       
                   
          
            )


RELATION_ROLE_CHOICES = (('variant', 'Variant'),
                         ('antonym', 'Antonym'),
                         ('synonym', 'Synonym'),
                         ('seealso', 'See Also'),
                         ('homophone', 'Homophone'),
                         )

class Relation(models.Model):
    """A relation between two glosses"""
    
    source = models.ForeignKey(Gloss, related_name="relation_sources")
    target = models.ForeignKey(Gloss, related_name="relation_targets")
    role = models.CharField(max_length=20, choices=RELATION_ROLE_CHOICES)  
                # antonym, synonym, cf (what's this? - see also), var[b-f]
                               # (what's this - variant (XXXa is the stem, XXXb is a variant)
                       
    class Admin:
        list_display = [ 'source', 'role','target']
        search_fields = ['source__idgloss', 'target__idgloss']        
        
    class Meta:
        ordering = ['source']
 
