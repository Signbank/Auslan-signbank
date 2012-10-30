from django.contrib import admin 
from models import Video, GlossVideo 

#admin.site.register(Video)

class GlossVideoAdmin(admin.ModelAdmin):
    search_fields = ['^gloss_sn']
    
admin.site.register(GlossVideo, GlossVideoAdmin)