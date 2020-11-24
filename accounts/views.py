from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from django.http import HttpResponse
import os
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

emp_name_handle = open(os.path.join(BASE, 'employee.txt'))
first = emp_name_handle.read()
name_list = first.split()


def register(request):
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
        mode = request.POST['mode']
        goal = request.POST['goal']
        instauser = request.POST['instauser']

        height = (((float(foot) * 12) + float(inch)) * 2.54) / 100
        bmi = float(weight) / (height * height)
        name = first_name + ' ' + last_name
        lead, created = models.AllLead.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                             state=state, weight=weight,
                                                             height=height, gender=gender,

                                                             contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                             created=datetime.datetime.now(), status='fresh')
        lead.save()

        lead2, created = models.Manager.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                              state=state, weight=weight,
                                                              height=height, gender=gender,

                                                              contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                              created=datetime.datetime.now(), status='fresh')
        lead2.save()

        return redirect("/token")


    else:
        return render(request,'register.html')
        # ("allname=Saurabh.objects.all()\n"
        # "        return render(request,'login.html',{'allname':allname})")


def show(request):
    name = models.Manager.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.Manager.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})


def show_saurabh(request):
    name = models.Saurabh.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.Saurabh.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})


def token(request):
    return render(request,'token.html')


def show_vikas(request):
    name = models.Vikas.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.Vikas.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})


def show_userone(request):
    name = models.UserOne.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.UserOne.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})


def show_usertwo(request):
    name = models.UserTwo.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.UserTwo.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})


def show_userthree(request):
    name = models.UserThree.objects.all()
    fresh = 0
    pending = 0
    closed = 0
    other = 0

    for item in models.UserThree.objects.all():
        if item.status == 'fresh':
            fresh += 1
        elif item.status == 'pending':
            pending += 1
        elif item.status == 'closed':
            closed += 1
        else:
            other += 1
    return render(request, 'main_lead_display.html',
                  {'name': name, "fresh": fresh, "pending": pending, "closed": closed, "other": other})

