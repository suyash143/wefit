from django.db import models
from accounts.models import *
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


class information(models.Model):
    lead=models.OneToOneField(Final,on_delete=models.CASCADE)
    dob=models.DateField(null=True,blank=True )
    plan=models.CharField(max_length=250,blank=True,null=True)
    smoking=models.CharField(max_length=100,blank=True,null=True)
    drinking=models.CharField(max_length=100,blank=True,null=True)
    start_of_plan = models.DateTimeField(null=True, blank=True)
    photo_link = models.URLField(max_length=400, null=True, blank=True)

    dietitian_assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    daily_diet = models.TextField(null=True, blank=True)
    sports = models.CharField(max_length=250, null=True, blank=True)
    supplements = models.CharField(max_length=250, null=True, blank=True)
    supplements_wish = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=120, null=True, blank=True)
    diet = models.CharField(max_length=120, null=True, blank=True)
    previous_workout = models.TextField(null=True, blank=True)
    disease = models.TextField(null=True, blank=True)
    meal_prep = models.CharField(max_length=200, null=True, blank=True)
    meds = models.TextField(null=True, blank=True)
    equipments = models.TextField(null=True, blank=True)
    injury = models.TextField(null=True, blank=True)


@receiver(post_save, sender=Final)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        information.objects.create(lead=instance)


@receiver(post_save, sender=Final)
def save_user_profile(sender, instance, **kwargs):
    instance.information.save()