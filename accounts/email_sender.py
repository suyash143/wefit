from django.core.mail import send_mail
import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def target_reset(request):
    first=User.objects[0]
    print(first)
    x



