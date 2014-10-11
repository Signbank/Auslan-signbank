from signbank.registration.models import *
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
   list_display = ['user', 'australian', 'auslan_user', 'deaf', 'background', 'researcher_credentials']
   readonly_fields = ['user', 'australian', 'auslan_user', 'deaf', 'yob', 'postcode', 'background', 'researcher_credentials', 'learned', 'schooltype', 'school', 'teachercomm']
   list_filter = ['australian', 'auslan_user', 'deaf']
admin.site.register(UserProfile, UserProfileAdmin)
