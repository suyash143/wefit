from django.http import HttpResponse
from . import models
from django.core.exceptions import PermissionDenied
import csv

def export_csv(arg):
    response=HttpResponse(content_type='text/csv')

    writer=csv.writer(response)
    writer.writerow(['Name','number','email','city','state','weight','height','bmi','gender','contact','type','created'
                     ,'rescheduled','comment','status','substatus','assigned'])

    for member in models.Final.objects.all().values_list('name','number','email','city','state','weight','height','bmi','gender','contact','type','created'
                     ,'rescheduled','comment','status','substatus','assigned'):
        writer.writerow(member)

    response['Content-Disposition']='attachement; filename="members.csv"'
    '''models.Final.objects.all().values_list('name','number','email','city','state','weight','height','bmi','gender','contact','type','created'
                     ,'rescheduled','comment','status','substatus','assigned')'''
    return response

a=models.Final.objects.all()