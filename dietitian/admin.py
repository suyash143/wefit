from django.contrib import admin
from . import models


class InformationOrder(admin.ModelAdmin):
    list_display = ['pk','name','number','email','created','assigned','paid']


admin.site.register(models.Information,InformationOrder)

# Register your models here.
