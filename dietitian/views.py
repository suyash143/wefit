from . import models
import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.db import connection

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

from django.contrib.staticfiles import finders
from django.core import serializers
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from random import choice
from . forms import ClientPicture,UpdatePicture
from string import digits, ascii_letters
import random




def client_register(request):
    form = ClientPicture()
    context = {'form': form}

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        number = request.POST['number']
        city = request.POST['city']
        state = request.POST['state']
        weight = request.POST['weight']
        foot = request.POST.get('foot', 5)
        inch = request.POST.get('inch', 8)
        gender = request.POST['gender']
        goal = request.POST.get('goal', 'weight_loss')
        country = request.POST.get('country', None)
        insta_user = request.POST.get('insta_user', None)
        zipcode = request.POST.get('zipcode', None)
        sports = request.POST.get('sports', 'No')
        supplements = request.POST.get('supplements', 'No')
        supplements_wish = request.POST.get('supplements_wish', 'Yes')
        place = request.POST['place']
        diet = request.POST['diet']
        what_workout = request.POST.get('what_workout', 'No')
        workout_frequency = request.POST.get('workout_frequency', "0")
        previous_workout = f"{what_workout} , for {workout_frequency} Hours in week"
        disease = request.POST.get('disease', None)
        meal_prep = request.POST.get('meal_prep', None)
        meds = request.POST.get('meds', None)
        equipments = request.POST.get('equipments', None)
        injury = request.POST.get('injury', None)
        telegram = request.POST.get('telegram', None)
        front_profile = request.POST.get('front_profile', None)
        left_profile = request.POST.get('left_profile', None)
        right_profile = request.POST.get('right_profile', None)
        back_profile = request.POST.get('back_profile', None)

        height = (((float(foot) * 12) + float(inch)) * 2.54) / 100
        bmi = float(weight) / (height * height)
        name = first_name + ' ' + last_name

        print(request.FILES)

        form = ClientPicture(request.POST, request.FILES)
        if form.is_valid():

            form.save()

            latest = models.Information.objects.latest('pk')
            form.created = datetime.datetime.now()
            latest.name = name
            latest.goal = goal
            latest.created = datetime.datetime.now()
            latest.height = height
            latest.bmi = bmi
            latest.previous_workout = previous_workout
            s = ''
            for i in range(6):
                s += random.choice(digits + ascii_letters)
            latest.client_secret = s
            latest.save()

        return redirect('client_token')
    return render(request, 'client_register.html', context)


def client_token(request):
    return render(request,'client_token.html')


def clients(request):

    name = models.Information.objects.all().order_by('-created')
    name_paginator = Paginator(name, 130)
    page_num = request.GET.get('page')
    page = name_paginator.get_page(page_num)
    if request.method == "POST" and 'id' in request.POST:
        id = request.POST.get('id')
        name = models.Information.objects.get(id=id)

        request.session['id'] = id

        return redirect('client_edit')

    return render(request,'clients.html', {'page': page})

def client_edit(request):
    form = UpdatePicture()
    context = {'form': form}
    id = request.session.get('id')

    users = User.objects.all().filter(is_staff=0)

    name = models.Information.objects.get(id=id)
    current_user = request.user.get_short_name()
    m = name.height
    tot_feet = m * 3.2808
    tot_inch = m * 39.37

    inch = round(tot_inch - int(tot_feet) * 12)
    feet = int(tot_feet)
    bmi = name.bmi
    cls = ''
    if bmi < 16:
        cls = "severely underweight"

    elif 16 <= bmi < 18.5:
        cls = "Underweight"

    elif 18.5 <= bmi < 25:
        cls = " Normal Weight"

    elif 25 <= bmi < 30:
        cls = "Overweight"

    elif bmi >= 30:
        cls = "Obese"
    person_stat = {'feet': feet, 'inch': inch, 'cls': cls}
    if request.method == "POST":

        updater = models.Information.objects.get(id=id)
        if updater.start_of_plan is None:
            form = UpdatePicture(request.FILES, instance=updater)
            if form.is_valid():
                form.save()

            payment_screenshot = request.FILES.get('payment_screenshot', None)
            rescheduled = request.POST.get('rescheduled', None)
            payment_method = request.POST.get('payment_method', None)
            payment_date = request.POST.get('payment_date', None)
            paid = request.POST.get('paid', 0)
            assigned_id = request.POST.get('assigned', None)
            updater.payment_method = payment_method
            updater.payment_date = payment_date
            updater.payment_screenshot = payment_screenshot
            updater.start_of_plan = rescheduled
            updater.paid = paid
            updater.assigned = User.objects.get(pk=assigned_id)
            trainer = User.objects.get(pk=assigned_id)
            updater.save()

            '''subject = 'Welcome to Fit Simran Transformation plan'
            data = models.Information.objects.get(id=id)
            client_secret = data.client_secret
            html_message = render_to_string('email.html',
                                            {'data': data, 'trainer': trainer, 'client_secret': client_secret})
            plain_message = strip_tags(html_message)
            from_email = 'connect@fitsimran.com'
            to = updater.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            
            trainer_subject = 'New Client Alert !'
            trainer_email = trainer.email
            trainer_html_message = render_to_string('email_trainer.html')
            trainer_plain_message = strip_tags(trainer_html_message)
            mail.send_mail(trainer_subject, trainer_plain_message, from_email, [trainer_email],
                           html_message=trainer_html_message)'''

            return redirect('clients')
        else:
            assigned_id = request.POST.get('assigned', None)
            updater.assigned = User.objects.get(pk=assigned_id)
            return redirect('clients')
    if name.start_of_plan is not None:
        return render(request, 'client_edit.html',
                      {'name': name, 'users': users, 'person_stat': person_stat, 'start_of_plan': False})
    return render(request, 'client_edit.html',
                  {'name': name, 'users': users, 'person_stat': person_stat, 'start_of_plan': True, 'form': form})


def dietitian_dashboard(request):
    return render(request,'dietitian_dashboard.html')