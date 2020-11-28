from django.contrib import admin
from. models import *

from. import add_admin_use





class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','assigned','created','status','contact','name','bmi','city','rescheduled','number']
    actions = add_admin_use.action_grabber()

    def transfer_to_saurabh(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=4))

    transfer_to_saurabh.short_description = "Transfer to Saurabh"

admin.site.register(Final,OrderAdmin)

