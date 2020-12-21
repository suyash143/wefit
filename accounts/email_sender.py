
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wefit.settings")
import django
django.setup()
from accounts import views

from django.shortcuts import render, redirect

views.email_sender()