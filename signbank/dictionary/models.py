"""Models for the Auslan database.

These are refactored from the original database to 
normalise the data and hopefully make it more
manageable.  

"""

from django.db.models import Q
from django.db import models
from django.conf import settings
from django.http import Http404 
import tagging

import sys, os
import json

#from signbank.video.models import GlossVideo

#from models_legacy import Sign


class Translation(models.Model):
    """An English translations of Auslan glosses"""
     
    gloss = models.ForeignKey("Gloss")
    translation = models.ForeignKey("Keyword")
    index = models.IntegerField("Index")
    
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
        ordering = ['gloss', 'index']
        
    class Admin:
        list_display = ['gloss', 'translation']
        search_fields = ['gloss__idgloss']
    
    
    
class Keyword(models.Model):
    """An english keyword that will be a translation of a sign"""
    
    def __str__(self):
        return self.text
    
    text = models.CharField(max_length=100, unique=True)
    
    def inWeb(self):
        """Return True if some gloss associated with this
        keyword is in the web version of the dictionary"""
        
        return len(self.translation_set.filter(gloss__inWeb__exact=True)) != 0
            
    class Meta:
        ordering = ['text']
        
    class Admin:
        search_fields = ['text']
        
        
        
    def match_request(self, request, n):
        """Find the translation matching a keyword request given an index 'n'
        response depends on login status
        Returns a tuple (translation, count) where count is the total number
        of matches."""
        
        if request.user.has_perm('dictionary.search_gloss'):
            alltrans = self.translation_set.all()
        else:
            alltrans = self.translation_set.filter(gloss__inWeb__exact=True)
        
        # if there are no translations, generate a 404
        if len(alltrans) == 0:
            raise Http404
        
        # take the nth translation if n is in range
        # otherwise take the last
        if n-1 < len(alltrans):
            trans = alltrans[n-1]
        else:
            trans = alltrans[len(alltrans)-1]
        
        return (trans, len(alltrans))
    
    
defn_role_choices = (('general', 'General Definition'),
                     ('noun', 'As a Noun'),
                     ('verb', 'As a Verb or Adjective'), 
                     ('deictic', 'As a Pointing Sign'),
                     ('interact', 'Interactive'),
                     ('modifier', 'As Modifier'),
                     ('question', 'As Question'),
                     ('popexplain', 'Popular Explanation'),
                     ('augment', 'Augmented Meaning'),
                     ('note', 'Note'),
                     ('privatenote', 'Private Note')
                     )


class Definition(models.Model):
    """An English text associated with an Auslan glosses"""
    
    def __str__(self):
        return str(self.gloss)+"/"+self.role
        
    gloss = models.ForeignKey("Gloss")
    text = models.TextField()
    role = models.CharField(max_length=20, choices=defn_role_choices)  
    count = models.IntegerField()
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['gloss', 'role', 'count']
        
    class Admin:
        list_display = ['gloss', 'role', 'count', 'text']
        list_filter = ['role']
        search_fields = ['gloss__idgloss']
        
class Language(models.Model):
    """A sign language name"""
        
    class Meta:
        ordering = ['name']
        
    name = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Dialect(models.Model):
    """A dialect name - a regional dialect of a given Language"""
    
    class Meta:
        ordering = ['language', 'name']
    
    language = models.ForeignKey(Language)
    name = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return self.language.name+"/"+self.name  
  
handshapeChoices = (('notset', 'No Value Set'),
                    ('0.1', 'Round'),
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
                     
locationChoices = ( (-1, 'No Value Set'),
                    (0, 'N/A'),
                    (1, 'Top of head'),
                    (2, 'Forehead'),
                    (3, 'Temple'),
                    (4, 'Eye'),
                    (5, 'Nose'),
                    (6, 'Whole of face'),
                    (7, 'Cheekbone'),
                    (8, 'Ear or side of head'),
                    (9, 'Cheek'),
                    (10, 'Mouth and lips'),
                    (11, 'Chin'),
                    (12, 'Neck'),
                    (13, 'Shoulder'),
                    (14, 'Chest'),
                    (28, 'High neutral space'),  # should be after 14
                    (15, 'Stomach'),
                    (29, 'Neutral space'),  # should be after 15
                    (16, 'Waist'),
                    (17, 'Below waist'),
                    (18, 'Upper arm'),
                    (19, 'Elbow'),
                    (20, 'Pronated forearm'),
                    (21, 'Supinated forearm'),
                    (22, 'Pronated wrist'),
                    (23, 'Spinated wrist'),
                    (24, 'Back of hand'),
                    (25, 'Palm'),
                    (26, 'Edge of hand'),
                    (27, 'Fingertips'),
                    )

# these are values for prim2ndloc fin2ndloc introduced for BSL, the names might change
BSLsecondLocationChoices = (
                    ('notset', 'No Value Set'),
                    ('0', 'N/A'),
                    ('back', 'Back'),
                    ('palm', 'Palm'),
                    ('radial', 'Radial'),
                    ('ulnar', 'Ulnar'),
                    ('fingertip(s)', 'Fingertips'),
                    ('root', 'Root')
                    )

palmOrientationChoices = (
                    ('notset', 'No Value Set'),
                    ('prone','Prone'),
                    ('neutral', 'Neutral'),
                    ('supine', 'Supine'),
                    ('0', 'N/A'),      
                          )

relOrientationChoices = (
                    ('notset', 'No Value Set'),
                    ('palm', 'Palm'),
                    ('back', 'Back'),
                    ('root', 'Root'), 
                    ('radial', 'Radial'),
                    ('ulnar', 'Ulnar'),
                    ('fingertip(s)', 'Fingertips'),
                    ('0', 'N/A'),  
                        )

class Gloss(models.Model):
    
    class Meta:
        verbose_name_plural = "Glosses"
        ordering = ['idgloss']
        permissions = (('update_video', "Can Update Video"),
                       ('search_gloss', 'Can Search/View Full Gloss Details'),
                        )

        
    def __str__(self):
        return "%s-%s" % (self.sn, self.idgloss)
    
    idgloss = models.CharField("Sign Entry Name", max_length=50, help_text="""
    This is the unique identifying name of an entry of a sign form in the
database. No two Sign Entry Names can be exactly the same, but a "Sign
Entry Name" can be (and often is) the same as the Annotation Idgloss.""")    
  
    annotation_idgloss = models.CharField("Annotation Idgloss", blank=True, max_length=30, help_text="""
    This is the name of a sign used by annotators when glossing the corpus in
an ELAN annotation file. The Annotation Idgloss may be the same for two or
more entries (each with their own 'Sign Entry Name'). If two sign entries
have the same 'Annotation Idgloss' that means they differ in form in only
minor or insignificant ways that can be ignored.""") 
    # the idgloss used in transcription, may be shared between many signs


    # languages that this gloss is part of
    language = models.ManyToManyField(Language)

    # these language fields are subsumed by the language field above
    bsltf = models.NullBooleanField("BSL sign", null=True, blank=True)
    asltf = models.NullBooleanField("ASL sign", null=True, blank=True)

    # these fields should be reviewed - do we put them in another class too?
    aslgloss = models.CharField("ASL gloss", blank=True, max_length=50) # American Sign Language gloss
    asloantf = models.NullBooleanField("ASL loan sign", null=True, blank=True)
 
    # loans from british sign language
    bslgloss = models.CharField("BSL gloss", max_length=50, blank=True) 
    bslloantf = models.NullBooleanField("BSL loan sign", null=True, blank=True)
 
    ########
    
    # one or more regional dialects that this gloss is used in
    dialect = models.ManyToManyField(Dialect)
    
    
    blend = models.CharField("Blend of", max_length=100, null=True, blank=True) # This field type is a guess.
    blendtf = models.NullBooleanField("Blend", null=True, blank=True)
    
    compound = models.CharField("Compound of", max_length=100, blank=True) # This field type is a guess.
    comptf = models.NullBooleanField("Compound", null=True, blank=True)
    

    # Phonology fields
    
    domhndsh = models.CharField("Dominant Hand Shape", blank=True,  null=True, choices=handshapeChoices, max_length=5)  
    subhndsh = models.CharField("Subordinate Hand Shape", null=True, choices=handshapeChoices, blank=True, max_length=5) 
    
    final_domhndsh = models.CharField("Final Dominant Hand Shape", blank=True,  null=True, choices=handshapeChoices, max_length=5)  
    final_subhndsh = models.CharField("Final Subordinate Hand Shape", null=True, choices=handshapeChoices, blank=True, max_length=5) 
 
    locprim = models.IntegerField("Primary Location", choices=locationChoices, null=True, blank=True) 
    final_loc = models.IntegerField("Final Location", choices=locationChoices, null=True, blank=True) 
    
    locsecond = models.IntegerField("Secondary Location", choices=locationChoices, null=True, blank=True) 
    
    initial_secondary_loc = models.CharField("Initial Secondary Location (BSL)", max_length=20, choices=BSLsecondLocationChoices, null=True, blank=True) 
    final_secondary_loc = models.CharField("Final Secondary Location (BSL)", max_length=20, choices=BSLsecondLocationChoices, null=True, blank=True) 
     
    
    initial_palm_orientation = models.CharField("Initial Palm Orientation", max_length=20, null=True, blank=True, choices=palmOrientationChoices) 
    final_palm_orientation = models.CharField("Final Palm Orientation", max_length=20, null=True, blank=True, choices=palmOrientationChoices)
  
    initial_relative_orientation = models.CharField("Initial Relative Orientation", null=True, max_length=20, blank=True, choices=relOrientationChoices) 
    final_relative_orientation = models.CharField("Final Relative Orientation", null=True, max_length=20, blank=True, choices=relOrientationChoices)
 
    
    inWeb = models.NullBooleanField("In the Web dictionary", default=False)
    isNew = models.NullBooleanField("Is this a proposed new sign?", null=True, default=False)
    
    inittext = models.CharField(max_length="50", blank=True) 

    morph = models.CharField("Morphemic Analysis", max_length=50, blank=True)  

    sedefinetf = models.TextField("Signed English definition available", null=True, blank=True)  # TODO: should be boolean
    segloss = models.CharField("Signed English gloss", max_length=50, blank=True,  null=True) 

    sense = models.IntegerField("Sense Number", null=True, blank=True, help_text="If there is more than one sense of a sign enter a number here, all signs with sense>1 will use the same video as sense=1") 
    sense.list_filter_sense = True

    sn = models.IntegerField("Sign Number", help_text="Sign Number must be a unique integer and defines the ordering of signs in the dictionary", null=True, blank=True, unique=True)   
            # this is a sign number - was trying
            # to be a primary key, also defines a sequence - need to keep the sequence
            # and allow gaps between numbers for inserting later signs
            
    StemSN = models.IntegerField(null=True, blank=True) 

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Gloss._meta.fields]

    def navigation(self, is_staff):
        """Return a gloss navigation structure that can be used to
        generate next/previous links from within a template page"""
    
        result = dict() 
        result['next'] = self.next_dictionary_gloss(is_staff)
        result['prev'] = self.prev_dictionary_gloss(is_staff)
        return result
    
    def admin_next_gloss(self):
        """next gloss in the admin view, shortcut for next_dictionary_gloss with staff=True"""

        return self.next_dictionary_gloss(True)
        
    def admin_prev_gloss(self):
        """previous gloss in the admin view, shortcut for prev_dictionary_gloss with staff=True"""

        return self.prev_dictionary_gloss(True)

        
    def next_dictionary_gloss(self, staff=False):
        """Find the next gloss in dictionary order"""
        if self.sn == None:
            return None
        elif staff:
            set =  Gloss.objects.filter(sn__gt=self.sn).order_by('sn')
        else:
            set = Gloss.objects.filter(sn__gt=self.sn, inWeb__exact=True).order_by('sn')
        if set:
            return set[0]
        else:
            return None
 
    def prev_dictionary_gloss(self, staff=False):
        """Find the previous gloss in dictionary order"""
        if self.sn == None:
            return None
        elif staff:
            set = Gloss.objects.filter(sn__lt=self.sn).order_by('-sn')
        else:
            set = Gloss.objects.filter(sn__lt=self.sn, inWeb__exact=True).order_by('-sn')
        if set:
            return set[0]
        else:
            return None     
             
    def get_absolute_url(self):
        return "/dictionary/gloss/%s.html" % self.idgloss
    
    
    def homophones(self):
        """Return the set of homophones for this gloss ordered by sense number"""
        
        if self.sense == 1:
            relations = Relation.objects.filter(role="homophone", target__exact=self).order_by('source__sense')
            homophones = [rel.source for rel in relations]
            homophones.insert(0,self)
            return homophones
        elif self.sense > 1:
            # need to find the root and see how many senses it has
            homophones = self.relation_sources.filter(role='homophone', target__sense__exact=1)
            if len(homophones) > 0:   
                root = homophones[0].target
                return root.homophones()
        return []


    def get_video_gloss(self):
        """Work out the gloss that might have the video for this sign, usually the sign number but
        if we're a sense>1 then we look at the homophone with sense=1
        Return the gloss instance."""
        
        if self.sense > 1:
            homophones = self.relation_sources.filter(role='homophone', target__sense__exact=1)
            # should be only zero or one of these
            if len(homophones) > 0:   
                return homophones[0].target
        return self
                
    def get_video(self):
        """Return the video object for this gloss or None if no video available"""
        
        video_with_gloss = self.get_video_gloss()
        
        try:
            video = video_with_gloss.glossvideo_set.get(version__exact=0)
            return video
        except:
            return None
        
    def count_videos(self):
        """Return a count of the number of videos we have 
        for this video - ie. the number of versions stored"""
        
        
        video_with_gloss = self.get_video_gloss()
        
        return video_with_gloss.glossvideo_set.count()
    
    
    def get_video_url(self):
        """return  the url of the video for this gloss which may be that of a homophone"""
         
         
        video = self.get_video()
        if video != None:
            return video.get_absolute_url()
        else:
            return ""
        
    def has_video(self):
        """Test to see if the video for this sign is present"""
        
        return self.get_video() != None
    
    def published_definitions(self):
        """Return a query set of just the published definitions for this gloss"""
        
        return self.definition_set.filter(published__exact=True)
    
    
    def definitions(self):
        """gather together the definitions for this gloss"""
    
        defs = dict()
        for d in self.definition_set.all().order_by('count'):
            if not defs.has_key(d.role):
                defs[d.role] = []
            
            defs[d.role].append(d.text)
        return defs
    
    
    def options_to_json(self, options):
        """Convert an options list to a json dict"""
        
        result = []
        for k, v in options:
            result.append('"%s":"%s"' % (k, v))
        return "{" + ",".join(result) + "}"
    
    def handshape_choices_json(self):
        """Return JSON for the handshape choice list"""
        
        return self.options_to_json(handshapeChoices)
    
    
    def location_choices_json(self):
        """Return JSON for the location choice list"""
        
        return self.options_to_json(locationChoices)
    
    def palm_orientation_choices_json(self):
        """Return JSON for the palm orientation choice list"""
        
        return self.options_to_json(palmOrientationChoices)

    def relative_orientation_choices_json(self):
        """Return JSON for the relative orientation choice list"""
        
        return self.options_to_json(relOrientationChoices)
    
    def secondary_location_choices_json(self):
        """Return JSON for the secondary location (BSL) choice list"""
        
        return self.options_to_json(BSLsecondLocationChoices)
    
     
    def definition_role_choices_json(self):
        """Return JSON for the definition role choice list"""
        
        return self.options_to_json(defn_role_choices)
    
    def language_choices(self):
        """Return JSON for langauge choices"""
        
        d = dict()
        for l in Language.objects.all():
            d[l.name] = l.name

        return json.dumps(d)

    def dialect_choices(self):
        """Return JSON for dialect choices"""
        
        d = dict()
        for l in Dialect.objects.all():
            d[l.name] = l.name

        return json.dumps(d)
    

# register Gloss for tags
try:
    tagging.register(Gloss)
except tagging.AlreadyRegistered:
    pass

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
 
