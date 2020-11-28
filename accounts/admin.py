from django.contrib import admin
from. models import *

from. import add_admin_use





class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','assigned','created','status','contact','name','bmi','city','rescheduled','number']
    actions = add_admin_use.action_grabber()

admin.site.register(Final,OrderAdmin)

