
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wefit.settings")
import django
django.setup()
from accounts.views import email_sender

from django.shortcuts import render, redirect

email_sender()