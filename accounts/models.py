from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
import datetime

class AllLead(models.Model):

    name=models.CharField(max_length=200)
    number=models.IntegerField()
    email=models.EmailField()
    city=models.CharField(max_length=300,null=True)
    state = models.CharField(max_length=500, null=True)
    insta_user=models.CharField(max_length=200)
    weight=models.FloatField()
    height=models.FloatField()
    bmi=models.FloatField()
    gender=models.CharField(max_length=50,null=True)
    contact=models.CharField(max_length=220)
    type=models.CharField(max_length=200)
    created=models.DateTimeField()
    rescheduled=models.DateTimeField(null=True,blank=True)
    comment = models.TextField(null=True)
    status = models.CharField(max_length=300,null=True)
    substatus=models.CharField(max_length=300,null=True)
    assigned=models.CharField(max_length=300,null=True)


class Manager(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    email = models.EmailField()
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=500, null=True)
    insta_user = models.CharField(max_length=200)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    gender = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=220)
    type = models.CharField(max_length=200)
    created = models.DateTimeField()
    rescheduled = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True)
    status = models.CharField(max_length=300, null=True)
    substatus = models.CharField(max_length=300, null=True)
    assigned = models.CharField(max_length=300, null=True)



class Final(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    email = models.EmailField()
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=500, null=True)
    insta_user = models.CharField(max_length=200)
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    gender = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=220)
    type = models.CharField(max_length=200)
    created = models.DateTimeField()
    rescheduled = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True)
    status = models.CharField(max_length=300, null=True)
    substatus = models.CharField(max_length=300, null=True)
    assigned = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    purchased = models.IntegerField(null=True, blank=True,default=0)
    paid = models.IntegerField(null=True, blank=True,default=0)

class Info(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=500,blank=True,null=True)
    target=models.IntegerField(null=True,blank=True,default=0)
    birthdate=models.DateField(null=True, blank=True)
    profile=models.CharField(max_length=400,null=True,blank=True)
    target_achieved=models.IntegerField(null=True,blank=True,default=0)
    date_start=models.DateField(null=True, blank=True,default=datetime.date.today()- datetime.timedelta(days=datetime.date.today().weekday()))
    date_end=models.DateField(null=True, blank=True,default=datetime.date.today()-datetime.timedelta(days=datetime.date.today().weekday())+datetime.timedelta(days=6))


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Info.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.info.save()

@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: # just in case user is not specified
        instance.user.delete()


class Record(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    start_date=models.DateField(null=True, blank=True)
    end_date=models.DateField(null=True,blank=True)
    target=models.IntegerField(null=True,blank=True)
    achieved=models.IntegerField(null=True,blank=True)


class Questions(models.Model):
    category=models.TextField(null=True)
    questions=models.TextField(null=True)
    answers=models.TextField(null=True)