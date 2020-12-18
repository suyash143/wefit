from django.contrib import admin
from. models import *

from. import add_admin_use


admin.site.register(Info)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','assigned','created','status','contact','name','bmi','city','rescheduled','number']
    actions = add_admin_use.action_grabber()


    def transfer_to_divyansh(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=3))
    transfer_to_divyansh.short_description = 'Transfer to divyansh'
    def transfer_to_aryan(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=5))
    transfer_to_aryan.short_description = 'Transfer to aryan'
admin.site.register(Final,OrderAdmin)
