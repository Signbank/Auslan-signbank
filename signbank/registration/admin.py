from signbank.registration.models import *
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
   list_display = ['user', 'australian', 'auslan_user', 'deaf', 'yob', 'postcode']
   readonly_fields = ['user', 'australian', 'auslan_user', 'deaf', 'yob', 'postcode', 'background', 'learned', 'schooltype', 'school', 'teachercomm']
   list_filter = ['australian', 'auslan_user', 'deaf']
admin.site.register(UserProfile, UserProfileAdmin)
