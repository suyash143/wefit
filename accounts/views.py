from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from.models import Final
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
import pytz
from django.db import connection
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
        IST = pytz.timezone('Asia/Kolkata')
        lead, created = models.AllLead.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                             state=state, weight=weight,
                                                             height=height, gender=gender,

                                                             contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                             created=datetime.datetime.now(o), status='fresh')


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
    current_user=request.user.get_short_name()
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
    return render(request, 'edit_employee.html',{'id': id,'first_name':first_name,'last_name':last_name,'name':name,'current_user':current_user})


def report(request):
    if request.method=="POST":
        startdate=request.POST.get('startdate')
        todate=request.POST.get('todate')

        all_data=models.Final.objects.raw('select * from accounts_final where created between "'+startdate+'" and "'+todate+'"')
        all_total=0
        all_fresh = 0
        all_cancelled = 0
        all_closed = 0
        all_other = 0
        all_rescheduled = 0
        all_follow_up = 0
        for all_item in all_data:
            all_total+=1
            if all_item.status == 'fresh':
                all_fresh += 1
            elif all_item.status == 'cancelled':
                all_cancelled += 1
            elif all_item.status == 'closed':
                all_closed += 1
            elif all_item.status == 'rescheduled':
                all_rescheduled += 1
            elif all_item.status == 'follow_up':
                all_follow_up += 1
            else:
                all_other+=1
        all={'all_total':all_total,'all_fresh':all_fresh,'all_cancelled':all_cancelled,'all_closed':all_closed,'all_rescheduled':all_rescheduled,'all_follow_up':all_follow_up}

        names = User.objects.order_by('username').values('username').distinct()
        report_name=[]
        final={}
        for item in names:
            one=item['username']
            report_name.append(one)
            cursor = connection.cursor()
            cursor.execute('select id from auth_user where username = "'+one+'"')
            assigned_id=cursor.fetchall()
            all=0
            fresh = 0
            cancelled = 0
            closed = 0
            other = 0
            rescheduled = 0
            follow_up = 0
            user_data=models.Final.objects.raw('select * from accounts_final where (created between "'+startdate+'" and "'+todate+'") and assigned_id ="'+str(assigned_id[0][0])+'" ')
            for count in user_data:
                all+=1
                if count.status == 'fresh':
                    fresh += 1
                elif count.status == 'cancelled':
                    cancelled += 1
                elif count.status == 'closed':
                    closed += 1
                elif count.status == 'rescheduled':
                    rescheduled += 1
                elif count.status == 'follow_up':
                    follow_up += 1

                else:
                    other += 1
            final[f'{one}']={'all':all,'fresh': fresh, 'cancelled': cancelled, 'closed': closed, 'rescheduled': rescheduled,'follow_up':follow_up,'other':other}


        return render(request, 'report.html', {'all': all,'final':final,'user_data':user_data})
    else:
        all_data = models.Final.objects.raw('select * from accounts_final')
        return render(request,'report.html',{'all_data':all_data})