from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from pages.models import Page
from pages.admin import PageAdmin

publisher_admin = AdminSite('pageadmin')
publisher_admin.register(Page, PageAdmin)
publisher_admin.register(User, UserAdmin)
publisher_admin.register(Group, GroupAdmin)
