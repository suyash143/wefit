from django.contrib import admin
from. models import *

from. import add_admin_use


class RecordOrder(admin.ModelAdmin):
    list_display = ['user','start_date','end_date','achieved','username']

class InfoOrder(admin.ModelAdmin):
    list_display = ['user','mobile','address','target','birthdate','profile','target_achieved','is_dietitian', 'date_start' ,'date_end']

admin.site.register(Info,InfoOrder)
admin.site.register(Record,RecordOrder)
admin.site.register(Questions)
admin.site.register(Improvement)




class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk','assigned','created','status','contact','name','bmi','city','rescheduled','number']
    actions = add_admin_use.action_grabber()


    def transfer_to_divyansh(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=3))
    transfer_to_divyansh.short_description = 'Transfer to divyansh'
    def transfer_to_aryan(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=5))
    transfer_to_aryan.short_description = 'Transfer to aryan'
    def transfer_to_yash(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=8))
    transfer_to_yash.short_description = 'Transfer to yash'
    def transfer_to_atharva(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=9))
    transfer_to_atharva.short_description = 'Transfer to atharva'
    def transfer_to_pp(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=10))
    transfer_to_pp.short_description = 'Transfer to pp'
    def transfer_to_anuj(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=16))
    transfer_to_anuj.short_description = 'Transfer to anuj'
    def transfer_to_kuldeep(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=17))
    transfer_to_kuldeep.short_description = 'Transfer to kuldeep'
    def transfer_to_bhatia(self, request, queryset):
        all=queryset.values().all().update(assigned=User.objects.get(id=18))
    transfer_to_bhatia.short_description = 'Transfer to bhatia'
admin.site.register(Final,OrderAdmin)
