from django.contrib import admin
from. models import *

admin.site.register(Saurabh)


class OrderAdmin(admin.ModelAdmin):
    actions = ['transfer_to_saurabh']

    def transfer_to_saurabh(self, request, queryset):
        all=queryset.values().all()
        for item in all:

            name=item['name']
            number=item['number']
            email = item['email']
            insta_user = item['insta_user']
            weight = item['weight']
            height = item['height']
            bmi = item['bmi']
            city=item['city']
            state=item['state']
            contact = item['contact']
            gender=item['gender']
            type = item['type']
            created = item['created']
            rescheduled = item['rescheduled']

            lead,create = Saurabh.objects.get_or_create(name=name,number=number,email=email,insta_user=insta_user,weight=weight,height=height,
                                                bmi=bmi,contact=contact,type=type,gender=gender,city=city,state=state,created=created,rescheduled=rescheduled,status='fresh',assigned='Saurabh')

            lead.save()
    transfer_to_saurabh.short_description = "Transfer to Saurabh"


admin.site.register(Manager,OrderAdmin)



