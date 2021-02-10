from django.db import models
from accounts.models import *
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


class information(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(max_length=300, null=True)
    state = models.CharField(max_length=500, null=True)
    insta_user = models.CharField(max_length=200, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=220, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    goal = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    start_of_plan = models.DateTimeField(null=True, blank=True)
    photo_link = models.URLField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=300, null=True, blank=True)
    assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.IntegerField(null=True, blank=True, default=0)
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
    telegram = models.CharField(max_length=300, null=True, blank=True)
    workout = models.CharField(max_length=100, null=True, blank=True)
    workout_time = models.CharField(max_length=100, null=True, blank=True)
    gym = models.CharField(null=True, blank=True, max_length=150)
    payment_method = models.CharField(max_length=120, null=True, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    client_secret = models.CharField(max_length=30, null=True, blank=True)


@receiver(post_save, sender=Final)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        information.objects.create(lead=instance)


@receiver(post_save, sender=Final)
def save_user_profile(sender, instance, **kwargs):
    instance.information.save()