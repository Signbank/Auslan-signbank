# models-legacy.py
# 
# A model that covers the original database 
# this has been refactored into the current models
# but is kept here to support updating the 
# database if needed

from django.db import models
 

handedness_choices = (("One", "One"),("Two", "Two"), ("Double", "Double"))

class Sign(models.Model):
    
    alternate = models.BooleanField(blank=True, null=True)
    angcongtf = models.BooleanField(blank=True, null=True)
    animalstf = models.BooleanField(blank=True, null=True)
    annotation_idgloss = models.CharField(blank=True, max_length=30) 
    
   # ant1 = models.ForeignKey("self", db_column="ant1", related_name="antonym1", null=True) # antonym
   # ant2 = models.ForeignKey("self", db_column="ant2", related_name="antonym2", null=True) # antonym
   # ant3 = models.ForeignKey("self", db_column="ant3", related_name="antonym3", null=True) # antonym
    
    ant1 = models.TextField(blank=True)
    ant2 = models.TextField(blank=True)
    ant3 = models.TextField(blank=True)
    
    arithmetictf = models.BooleanField(blank=True, null=True)
    artstf = models.BooleanField(blank=True, null=True)
    
    aslgloss = models.TextField(blank=True) # This field type is a guess.
    asloantf = models.BooleanField(blank=True, null=True)
    asltf = models.BooleanField(blank=True, null=True)
    
    augment = models.TextField(blank=True) # This field type is a guess.
    auslextf = models.BooleanField(blank=True, null=True)
    begindirtf = models.BooleanField(blank=True, null=True)
    blend = models.TextField(blank=True) # This field type is a guess.
    blendtf = models.BooleanField(blank=True, null=True)
    bodyloctf = models.BooleanField(blank=True, null=True)
    bodyprtstf = models.BooleanField(blank=True, null=True)
    BookProb = models.BooleanField(blank=True, null=True)
    bslgloss = models.TextField(blank=True) # This field type is a guess.
    bslloantf = models.BooleanField(blank=True, null=True)
    bsltf = models.BooleanField(blank=True, null=True)
    carstf = models.BooleanField(blank=True, null=True)
    catholictf = models.BooleanField(blank=True, null=True)
    cathschtf = models.BooleanField(blank=True, null=True)
    cf1 = models.TextField(blank=True) # This field type is a guess.
    cf2 = models.TextField(blank=True) # This field type is a guess.
    cf3 = models.TextField(blank=True) # This field type is a guess.
    citiestf = models.BooleanField(blank=True, null=True)
    clothingtf = models.BooleanField(blank=True, null=True)
    colorstf = models.BooleanField(blank=True, null=True)
    comp = models.BooleanField(blank=True, null=True) 
    compound = models.CharField(max_length=100, blank=True) # This field type is a guess.
    comptf = models.BooleanField(blank=True, null=True)
    cookingtf = models.BooleanField(blank=True, null=True)
    CorrectionsAdditionsComments = models.TextField(blank=True) # This field type is a guess.
    crudetf = models.BooleanField(blank=True, null=True)
    daystf = models.BooleanField(blank=True, null=True)
    deaftf = models.BooleanField(blank=True, null=True)
    
    deictic1 = models.TextField(blank=True) # This field type is a guess.
    deictic1tf = models.BooleanField(blank=True, null=True)
    deictic2 = models.TextField(blank=True) # This field type is a guess.
    deictic2tf = models.BooleanField(blank=True, null=True)
    deictic3 = models.TextField(blank=True) # This field type is a guess.
    deictic3tf = models.BooleanField(blank=True, null=True)
    deictic4 = models.TextField(blank=True) # This field type is a guess.
    deictic4tf = models.BooleanField(blank=True, null=True)

    dirtf = models.BooleanField(blank=True, null=True)  
    domhndsh = models.CharField(blank=True, max_length=5) 
    domonly = models.BooleanField(blank=True, null=True) 
    doublehnd = models.BooleanField(blank=True, null=True) 
    doubtlextf = models.BooleanField(blank=True, null=True)
    drinkstf = models.BooleanField(blank=True, null=True)
    eductf = models.BooleanField(blank=True, null=True)
    enddirtf = models.BooleanField(blank=True, null=True)
    
    english1 = models.TextField(blank=True) # This field type is a guess.
    english10 = models.TextField(blank=True) # This field type is a guess.
    english10tf = models.BooleanField(blank=True, null=True)
    english11 = models.TextField(blank=True) # This field type is a guess.
    english11tf = models.BooleanField(blank=True, null=True)
    english12 = models.TextField(blank=True) # This field type is a guess.
    english12tf = models.BooleanField(blank=True, null=True)
    english1tf = models.BooleanField(blank=True, null=True)
    english2 = models.TextField(blank=True) # This field type is a guess.
    english2tf = models.BooleanField(blank=True, null=True)
    english3 = models.TextField(blank=True) # This field type is a guess.
    english3tf = models.BooleanField(blank=True, null=True)
    english4 = models.TextField(blank=True) # This field type is a guess.
    english4tf = models.BooleanField(blank=True, null=True)
    english5 = models.TextField(blank=True) # This field type is a guess.
    english5tf = models.BooleanField(blank=True, null=True)
    english6 = models.TextField(blank=True) # This field type is a guess.
    english6tf = models.BooleanField(blank=True, null=True)
    english7 = models.TextField(blank=True) # This field type is a guess.
    english7tf = models.BooleanField(blank=True, null=True)
    english8 = models.TextField(blank=True) # This field type is a guess.
    english8tf = models.BooleanField(blank=True, null=True)
    english9 = models.TextField(blank=True) # This field type is a guess.
    english9tf = models.BooleanField(blank=True, null=True)
    
    familytf = models.BooleanField(blank=True, null=True)
    feeltf = models.BooleanField(blank=True, null=True)
    fingersptf = models.BooleanField(blank=True, null=True)
    foodstf = models.BooleanField(blank=True, null=True)
    furntf = models.BooleanField(blank=True, null=True)
    general = models.TextField(blank=True) # This field type is a guess.
    gensigntf = models.BooleanField(blank=True, null=True)
    govtf = models.BooleanField(blank=True, null=True)
    groomtf = models.BooleanField(blank=True, null=True)
    
    handedness = models.CharField(max_length=10, choices=handedness_choices, blank=True) 
    
    healthtf = models.BooleanField(blank=True, null=True)
    
  # this field removed, contents are not text
  #   hns = models.TextField(blank=True) 
  
    idgloss = models.CharField(primary_key=True, max_length=50) 
    inCD = models.BooleanField(blank=True, null=True, default=False) 
    inittext = models.CharField(max_length="50", blank=True) 
    inittf = models.BooleanField(blank=True, null=True)
    InMainBook = models.BooleanField(blank=True, null=True)
    InSuppBook = models.BooleanField(blank=True, null=True)
    interact1 = models.TextField(blank=True) # This field type is a guess.
    interact1tf = models.BooleanField(blank=True, null=True)
    interact2 = models.TextField(blank=True) # This field type is a guess.
    interact2tf = models.BooleanField(blank=True, null=True)
    interact3 = models.TextField(blank=True) # This field type is a guess.
    interact3tf = models.BooleanField(blank=True, null=True)
    judgetf = models.BooleanField(blank=True, null=True)
    jwtf = models.BooleanField(blank=True, null=True)
    langactstf = models.BooleanField(blank=True, null=True)
    lawtf = models.BooleanField(blank=True, null=True)
    locdirtf = models.BooleanField(blank=True, null=True)
    marginaltf = models.BooleanField(blank=True, null=True)
    materialstf = models.BooleanField(blank=True, null=True)
    metalgtf = models.BooleanField(blank=True, null=True) 
    mindtf = models.BooleanField(blank=True, null=True) 
    
    modifier1 = models.TextField(blank=True) # This field type is a guess.
    modifier1tf = models.BooleanField(blank=True, null=True)
    modifier2 = models.TextField(blank=True) # This field type is a guess.
    modifier2tf = models.BooleanField(blank=True, null=True)
    modifier3 = models.TextField(blank=True) # This field type is a guess.
    modifier3tf = models.BooleanField(blank=True, null=True)
    
    moneytf = models.BooleanField(blank=True, null=True)

    morph = models.CharField(max_length=50, blank=True) 
    # removed - not plain text 
    #morphns = models.CharField(max_length=50, blank=True) # not used
    naturetf = models.BooleanField(blank=True, null=True)
    
    # definitions as nouns
    nom1 = models.TextField(blank=True) 
    nom1tf = models.BooleanField(blank=True, null=True)
    nom2 = models.TextField(blank=True)  
    nom2tf = models.BooleanField(blank=True, null=True)
    nom3 = models.TextField(blank=True)  
    nom3tf = models.BooleanField(blank=True, null=True)
    nom4 = models.TextField(blank=True) 
    nom4tf = models.BooleanField(blank=True, null=True)
    nom5 = models.TextField(blank=True)  
    nom5tf = models.BooleanField(blank=True, null=True)
    
    
    NotBkDBOnly = models.BooleanField(blank=True, null=True) 
    nswtf = models.BooleanField(blank=True, null=True)
    nthtf = models.BooleanField(blank=True, null=True)
    numbertf = models.BooleanField(blank=True, null=True)
    obscuretf = models.BooleanField(blank=True, null=True)
    obsoletetf = models.BooleanField(blank=True, null=True)
    onehand = models.BooleanField(blank=True, null=True)
    opaquetf = models.BooleanField(blank=True, null=True)
    ordertf = models.BooleanField(blank=True, null=True)
    orienttf = models.BooleanField(blank=True, null=True)
    otherreltf = models.BooleanField(blank=True, null=True)
    Palm_orientation = models.CharField(max_length=10, blank=True) # only used twice = Left
    para = models.BooleanField(blank=True, null=True) 
    peopletf = models.BooleanField(blank=True, null=True)
    physicalactstf = models.BooleanField(blank=True, null=True)
    PopExplain = models.TextField(blank=True) # This field type is a guess.
    propernametf = models.BooleanField(blank=True, null=True)
    qldtf = models.BooleanField(blank=True, null=True) # used in Queensland
    qualitytf = models.BooleanField(blank=True, null=True)
    quantitytf = models.BooleanField(blank=True, null=True)
    queries = models.TextField(blank=True) # This field type is a guess.
    question1 = models.TextField(blank=True) # This field type is a guess.
    question1tf = models.BooleanField(blank=True, null=True)
    question2 = models.TextField(blank=True) # This field type is a guess.
    question2tf = models.BooleanField(blank=True, null=True)
    questsigntf = models.BooleanField(blank=True, null=True)
    recreationtf = models.BooleanField(blank=True, null=True)
    reglextf = models.BooleanField(blank=True, null=True)
    religiontf = models.BooleanField(blank=True, null=True)
    restricttf = models.BooleanField(blank=True, null=True)
    roomstf = models.BooleanField(blank=True, null=True)
    saluttf = models.BooleanField(blank=True, null=True)
    satf = models.BooleanField(blank=True, null=True) # used in South Australia
    sedefinetf = models.TextField(blank=True)
    segloss = models.CharField(max_length=50, blank=True) 
    sensestf = models.BooleanField(blank=True, null=True)
    seonlytf = models.BooleanField(blank=True, null=True)
    setf = models.BooleanField(blank=True, null=True)
    sextf = models.BooleanField(blank=True, null=True)
    shapestf = models.BooleanField(blank=True, null=True)
    shoppingtf = models.BooleanField(blank=True, null=True)
    SpecialCore = models.TextField(blank=True) # This field type is a guess.
    sporttf = models.BooleanField(blank=True, null=True)
    stateschtf = models.BooleanField(blank=True, null=True)
    sthtf = models.BooleanField(blank=True, null=True)
    sym = models.TextField(blank=True) # This field type is a guess.
    
    #syn1 = models.ForeignKey("self", db_column="syn1", related_name="synonym1", null=True) 
    syn1 = models.TextField(blank=True)
    syn1tf = models.BooleanField(blank=True, null=True)
    #syn2 = models.ForeignKey("self", db_column="syn2", related_name="synonym2", null=True) 
    syn2 = models.TextField(blank=True)
    syn2tf = models.BooleanField(blank=True, null=True)
    #syn3 = models.ForeignKey("self", db_column="syn3", related_name="synonym3", null=True) 
    syn3 = models.TextField(blank=True)
    syn3tf = models.BooleanField(blank=True, null=True)
    
    tastf = models.BooleanField(blank=True, null=True) # is it used in Tasmania
    
    techtf = models.BooleanField(blank=True, null=True)
    telecomtf = models.BooleanField(blank=True, null=True)
    timetf = models.BooleanField(blank=True, null=True)
    tjspeculate = models.TextField(blank=True) # This field type is a guess.
    transltf = models.BooleanField(blank=True, null=True)
    transptf = models.BooleanField(blank=True, null=True)
    traveltf = models.BooleanField(blank=True, null=True)
    twohand = models.BooleanField(blank=True, null=True) 
    utensilstf = models.BooleanField(blank=True, null=True)
    varb = models.TextField(blank=True) # This field type is a guess.
    varc = models.TextField(blank=True) # This field type is a guess.
    vard = models.TextField(blank=True) # This field type is a guess.
    vare = models.TextField(blank=True) # This field type is a guess.
    varf = models.TextField(blank=True) # This field type is a guess.
    varlextf = models.BooleanField(blank=True, null=True)
    
    # definitions as verb
    verb1 = models.TextField(blank=True) # This field type is a guess.
    verb1tf = models.BooleanField(blank=True, null=True)
    verb2 = models.TextField(blank=True) # This field type is a guess.
    verb2tf = models.BooleanField(blank=True, null=True)
    verb3 = models.TextField(blank=True) # This field type is a guess.
    verb3tf = models.BooleanField(blank=True, null=True)
    verb4 = models.TextField(blank=True) # This field type is a guess.
    verb4tf = models.BooleanField(blank=True, null=True)
    verb5 = models.TextField(blank=True) # This field type is a guess.
    verb5tf = models.BooleanField(blank=True, null=True)
    
    victf = models.BooleanField(blank=True, null=True) # used in Victoria
    watf = models.BooleanField(blank=True, null=True) # used in Western Australia
    
    weathertf = models.BooleanField(blank=True, null=True)
    worktf = models.BooleanField(blank=True, null=True)
    
    ant1tf = models.BooleanField(blank=True, null=True)
    ant2tf = models.BooleanField(blank=True, null=True)
    ant3tf = models.BooleanField(blank=True, null=True)
    cf1tf = models.BooleanField(blank=True, null=True)
    cf2tf = models.BooleanField(blank=True, null=True)
    cf3tf = models.BooleanField(blank=True, null=True)
    
    locprim = models.IntegerField(blank=True) 
    locsecond = models.IntegerField(blank=True) 
    sense = models.IntegerField(blank=True, null=True) 
    sn = models.IntegerField(blank=True)  
    StemSN = models.IntegerField(null=True)  
 
    subhndsh = models.CharField(null=True, max_length=5)  # a value like 0.1 
    # codified somewhere as hand shapes
    
    def __str__(self):
        return self.idgloss
    
    class Meta:
        db_table = 'lexicon'
        ordering = ['idgloss']
        
    class Admin:
        list_display = ('idgloss', 'english1')
        ordering = ['idgloss']
        search_fields = ['^idgloss']
    
    

