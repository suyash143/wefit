from django.contrib import admin
from. models import *

admin.site.register(Saurabh)
admin.site.register(Vikas)
admin.site.register(UserOne)
admin.site.register(UserTwo)
admin.site.register(UserThree)



class OrderAdmin(admin.ModelAdmin):
    actions = ['transfer_to_saurabh','transfer_to_vikas','transfer_to_userone','transfer_to_usertwo','transfer_to_userthree']

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

    def transfer_to_vikas(self, request, queryset):
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

            lead,create = Vikas.objects.get_or_create(name=name,number=number,email=email,insta_user=insta_user,weight=weight,height=height,
                                                bmi=bmi,contact=contact,type=type,gender=gender,city=city,state=state,created=created,rescheduled=rescheduled,status='fresh',assigned='Vikas')

            lead.save()
    transfer_to_vikas.short_description = "Transfer to Vikas"

    def transfer_to_userone(self, request, queryset):
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

            lead,create = UserOne.objects.get_or_create(name=name,number=number,email=email,insta_user=insta_user,weight=weight,height=height,
                                                bmi=bmi,contact=contact,type=type,gender=gender,city=city,state=state,created=created,rescheduled=rescheduled,status='fresh',assigned='User_one')

            lead.save()
    transfer_to_userone.short_description = "Transfer to User One"


    def transfer_to_usertwo(self, request, queryset):
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

            lead,create = UserTwo.objects.get_or_create(name=name,number=number,email=email,insta_user=insta_user,weight=weight,height=height,
                                                bmi=bmi,contact=contact,type=type,gender=gender,city=city,state=state,created=created,rescheduled=rescheduled,status='fresh',assigned='User_Two')

            lead.save()
    transfer_to_usertwo.short_description = "Transfer to User Two"


    def transfer_to_userthree(self, request, queryset):
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

            lead,create = UserThree.objects.get_or_create(name=name,number=number,email=email,insta_user=insta_user,weight=weight,height=height,
                                                bmi=bmi,contact=contact,type=type,gender=gender,city=city,state=state,created=created,rescheduled=rescheduled,status='fresh',assigned='User Three')

            lead.save()
    transfer_to_userthree.short_description = "Transfer to User three"


admin.site.register(Manager,OrderAdmin)



