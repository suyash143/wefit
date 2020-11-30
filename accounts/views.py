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
        mode = request.POST.get('mode', 'whatsapp')
        goal = request.POST.get('goal', 'weight_loss')
        instauser = request.POST.get('instauser', None)

        height = (((float(foot) * 12) + float(inch)) * 2.54) / 100
        bmi = float(weight) / (height * height)
        name = first_name + ' ' + last_name
        lead, created = models.AllLead.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                             state=state, weight=weight,
                                                             height=height, gender=gender,

                                                             contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                             created=datetime.datetime.now(), status='fresh')


        lead3, created = models.Final.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                              state=state, weight=weight,
                                                              height=height, gender=gender,

                                                              contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                              created=datetime.datetime.now(), status='fresh')
        lead3.save()

        return redirect("/token")




    else:
        return render(request,'register.html')
        # ("allname=Saurabh.objects.all()\n"
        # "        return render(request,'login.html',{'allname':allname})")


def token(request):
    return render(request,'token.html')



def all(request):
    if request.user.is_authenticated:
        fresh = 0
        cancelled = 0
        closed = 0
        other = 0
        rescheduled=0
        follow_up=0
        user=request.user
        if request.user.is_staff:
            name=models.Final.objects.all()
        else:
            name=models.Final.objects.all().filter(assigned=user)
        for item in name:
            if item.status == 'fresh':
                fresh += 1
            elif item.status == 'cancelled':
                cancelled += 1
            elif item.status == 'closed':
                closed += 1
            elif item.status=='rescheduled':
                rescheduled +=1
            elif item.status=='follow_up':
                follow_up +=1

            else:
                other += 1

        if request.method=="POST":
            id=request.POST.get('id')

            request.session['id'] = id

            return redirect('edit_employee')
        context={'name':name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other,'rescheduled':rescheduled,'follow_up':follow_up}
        return render(request,'main_lead_display.html',context)
    else:
        return HttpResponse('<h1>Forbidden</h1><h2>Please Log in to view your data</h2>')



def edit_employee(request):
    id = request.session.get('id')
    name = models.Final.objects.get(id=id)
    first_name = name.name.split()[0]
    last_name = name.name.split()[1]
    request.session['id'] = id
    if request.method == "POST":
        updater = models.Final.objects.get(id=id)
        status = request.POST.get('status', None)
        substatus = request.POST.get('substatus', None)
        comment=f'{name.comment},  {request.POST.get("comment",None)}'
        rescheduled=request.POST.get('rescheduled', None)
        updater.status = status
        updater.substatus = substatus
        updater.comment=comment
        updater.rescheduled=rescheduled

        updater.save()
        return redirect('all')
    return render(request, 'edit_employee.html',{'id': id,'first_name':first_name,'last_name':last_name,'name':name})
