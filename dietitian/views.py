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
    if request.method == "POST" and 'details' in request.POST:

        updater = models.Information.objects.get(id=id)
        if updater.paid == 0:

            paid = request.POST.get('paid', 0)
            assigned_id = request.POST.get('assigned', None)

            updater.follow_up_next = request.POST.get('follow_up_next',None)
            comment=request.POST.get('comment',None)
            weight=request.POST.get('weight',None)
            time = datetime.date.today()
            follow_up_record=f"\n{time} - {comment}"+f"\n {updater.follow_up_record} "
            updater.follow_up_record=follow_up_record
            updater.paid = paid
            new_weight=f"\n{time} - {weight}"+f"\n {updater.weight}"
            updater.weight_record=new_weight
            updater.weight=weight
            status = request.POST.get('status', None)
            start_of_plan = request.POST.get('start_of_plan', None)
            type_of_plan = request.POST.get('type_of_plan', None)
            updater.status=status
            updater.paid_details=f'{time} : {paid}'
            updater.start_of_plan=start_of_plan
            updater.type_of_plan=type_of_plan
            updater.save()

            date_changer = models.Information.objects.get(id=id)

            if date_changer.end_of_plan is None:
                if type_of_plan == '4 Weeks':
                    date_changer.end_of_plan =time+datetime.timedelta(days = 28)
                    date_changer.save()

                elif type_of_plan == '8 Weeks':
                    date_changer.end_of_plan =time+datetime.timedelta(days = 56)
                    date_changer.save()

                elif type_of_plan == '100 Days':
                    date_changer.end_of_plan =time+datetime.timedelta(days = 100)
                    date_changer.save()
                elif type_of_plan == '4 Months':
                    date_changer.end_of_plan =time+datetime.timedelta(days=121)
                    date_changer.save()
                elif type_of_plan == '6 Months':
                    date_changer.end_of_plan =time+datetime.timedelta(days=182)
                    date_changer.save()
                elif type_of_plan == '12 Months':
                    date_changer.end_of_plan =time+datetime.timedelta(days=365)
                    date_changer.save()
                date_changer.save()
            else:
                date_changer.end_of_plan = time

            date_changer.save()

            return redirect('clients')
        else:

            assigned_id = request.POST.get('assigned', None)

            updater.follow_up_next = request.POST.get('follow_up_next', None)
            comment = request.POST.get('comment', None)
            weight = request.POST.get('weight', None)
            status=request.POST.get('status',None)

            time = datetime.date.today()
            follow_up_record = f"\n{time} - {comment}" + f"\n {updater.follow_up_record} "
            updater.follow_up_record = follow_up_record
            new_weight = f"\n{time} - {weight}" + f"\n {updater.weight_record}"
            updater.weight_record = new_weight
            updater.weight = weight
            updater.status=status
            updater.save()
            return redirect('clients')
    if name.start_of_plan is not None:
        return render(request, 'client_edit2.html',
                      {'name': name, 'users': users, 'person_stat': person_stat, 'start_of_plan': False})
    return render(request, 'client_edit2.html',
                  {'name': name, 'users': users, 'person_stat': person_stat, 'start_of_plan': True, 'form': form})


def dietitian_dashboard(request):
    return render(request,'dietitian_dashboard.html')


def follow_up(request):
    today=datetime.date.today()

    name = models.Information.objects.filter(follow_up_next__range=[today,"2100-01-31"],status='Active')
    name_paginator = Paginator(name, 130)
    page_num = request.GET.get('page')
    page = name_paginator.get_page(page_num)
    if request.method == "POST" and 'id' in request.POST:
        id = request.POST.get('id')
        name = models.Information.objects.get(id=id)

        request.session['id'] = id

        return redirect('client_edit')

    return render(request, 'clients.html', {'page': page})


def paid_details(request):
    id = request.session.get('id')
    updater=models.Information.objects.get(id=id)
    name=models.Information.objects.get(id=id)

    if request.POST and 'payment' in request.POST:
        new_paid = request.POST.get('new_paid')
        payment_date=request.POST.get('payment_date')
        new=int(new_paid)-updater.paid
        history=f'\n{updater.paid_details}\n{payment_date} : {new} ({new_paid})\n'
        updater.paid_details = history
        updater.paid=new_paid
        updater.save()
        return redirect('client_edit')
    return render(request,'client_payment.html',{'name': name})

