from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms


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







