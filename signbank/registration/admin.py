from signbank.registration.models import *
from django.contrib import admin
from django.core.urlresolvers import reverse

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'permissions', 'best_describes_you', 'australian', 'auslan_user', 'deaf', 'researcher_credentials']
    readonly_fields = ['user', 'australian', 'auslan_user', 'deaf', 'yob', 'postcode', 'best_describes_you', 'researcher_credentials', 'learned', 'schooltype', 'school', 'teachercomm']
    list_filter = ['australian', 'auslan_user', 'deaf']
   
    def permissions(self, obj):
        url = reverse('admin:auth_user_change', args=(obj.pk,))
        return '<a href="%s">View user</a>' % (url)
    permissions.allow_tags = True
   
admin.site.register(UserProfile, UserProfileAdmin)
