import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from .models import Final
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
import pytz
from datetime import date
from django.utils import timezone
from django.db import connection
import datetime
from . import utils
from django.core.paginator import *

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

        if models.Final.objects.filter(number=number).order_by('-id')[:100]:
            return redirect('/token')
        lead, created = models.AllLead.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                             state=state, weight=weight,
                                                             height=height, gender=gender,

                                                             contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                             created=datetime.datetime.now(), status='fresh')

        lead.save()
        lead3, created = models.Final.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                            state=state, weight=weight,
                                                            height=height, gender=gender,

                                                            contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                            created=datetime.datetime.now(), status='fresh')
        lead3.save()

        return redirect("/token")

    else:
        return render(request, 'register.html')


def token(request):
    return render(request, 'token.html')


def all(request):
    if request.user.is_authenticated:
        fresh = 0
        al = 0
        cancelled = 0
        closed = 0
        other = 0
        rescheduled = 0
        follow_up = 0
        acknowledged = 0
        pending_cancelled = 0
        unassigned = 0

        user = request.user

        if request.user.is_staff:

            name = models.Final.objects.all()

        else:
            name = models.Final.objects.all().filter(assigned=user)

        for item in name:
            al += 1
            if item.status == 'fresh':
                fresh += 1
            elif item.status == 'cancelled':
                cancelled += 1
            elif item.status == 'closed':
                closed += 1
            elif item.status == 'rescheduled':
                rescheduled += 1
            elif item.status == 'follow_up':
                follow_up += 1
            elif item.status == 'acknowledged':
                acknowledged += 1
            elif item.status == 'pending_cancelled':
                pending_cancelled += 1

            else:
                other += 1

            if item.assigned is None:
                unassigned += 1

        if request.method == "POST" and 'id' in request.POST:
            id = request.POST.get('id')
            name = models.Final.objects.get(id=id)
            if name.status == "fresh":
                name.status = "acknowledged"
                name.save()

            request.session['id'] = id

            return redirect('edit_employee')

        elif request.method == 'POST' and 'filter' in request.POST:
            filter_value = request.POST.get('filter_value', 'all')
            startdate = request.POST.get('startdate', '2015-01-02')
            todate = request.POST.get('todate', datetime.date.today())
            user_id = request.user.pk
            if request.user.is_staff:
                if filter_value == "fresh":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')

                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": fresh, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})

                elif filter_value == "closed":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": closed, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})
                elif filter_value == "rescheduled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': rescheduled, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': 0})
                elif filter_value == "cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": cancelled, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})
                elif filter_value == "follow_up":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': follow_up, 'acknowledged': 0, 'pending_cancelled': 0})

                elif filter_value == "acknowledged":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': acknowledged,
                                   'pending_cancelled': 0})

                elif filter_value == "pending_cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': pending_cancelled})
                else:
                    name = models.Final.objects.raw(
                        'select * from accounts_final where created between "' + startdate + '" and "' + todate + '"')
                    context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other,
                               'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                               'pending_cancelled': pending_cancelled}
                    return render(request, 'main_lead_display.html', context)
            else:
                if filter_value == "fresh":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": fresh, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})

                elif filter_value == "closed":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": closed, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})
                elif filter_value == "rescheduled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': rescheduled, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': 0})
                elif filter_value == "cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": cancelled, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0})
                elif filter_value == "follow_up":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': follow_up, 'acknowledged': 0, 'pending_cancelled': 0})

                elif filter_value == "acknowledged":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': acknowledged,
                                   'pending_cancelled': 0})

                elif filter_value == "pending_cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    return render(request, 'main_lead_display.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': pending_cancelled})

                else:
                    name = models.Final.objects.all().filter(assigned=user)
                    context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other,
                               'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                               'pending_cancelled': pending_cancelled}
                    return render(request, 'main_lead_display.html', context)

        context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other, 'al': al,
                   'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                   'pending_cancelled': pending_cancelled, 'unassigned': unassigned}

        return render(request, 'main_lead_display.html', context)
    else:
        return HttpResponse('<h1>Forbidden</h1><h2>Please Log in to view your data</h2>')


def edit_employee(request):
    id = request.session.get('id')
    name = models.Final.objects.get(id=id)
    first_name = name.name.split()[0]
    last_name = name.name.split()[1]
    request.session['id'] = id
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
        updater = models.Final.objects.get(id=id)

        status = request.POST.get('status', "acknowledged")
        substatus = request.POST.get('substatus', None)
        cancel_link = request.POST['cancel_link']
        comment = f'{name.comment},  {request.POST.get("comment", None)}'
        rescheduled = request.POST.get('rescheduled', None)
        updater.status = status
        updater.substatus = substatus
        updater.insta_user = cancel_link
        updater.comment = comment
        updater.rescheduled = rescheduled

        updater.save()
        return redirect('all')
    return render(request, 'edit_employee.html',
                  {'id': id, 'first_name': first_name, 'last_name': last_name, 'name': name,
                   'current_user': current_user, 'person_stat': person_stat})


def report(request):
    if request.method == "POST":
        startdate = request.POST.get('startdate')
        todate = request.POST.get('todate')

        all_data = models.Final.objects.raw(
            'select * from accounts_final where created between "' + startdate + '" and "' + todate + '"')
        all_total = 0
        all_fresh = 0
        all_cancelled = 0
        all_closed = 0
        all_other = 0
        all_rescheduled = 0
        all_follow_up = 0
        all_acknowledged = 0
        all_pending_cancelled = 0
        all_days3 = 0
        all_days7 = 0
        all_unassigned = 0
        for all_item in all_data:

            all_total += 1

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
            elif all_item.status == 'acknowledged':
                all_acknowledged += 1

            elif all_item.status == 'pending_cancelled':
                all_pending_cancelled += 1

            else:
                all_other += 1
            if 3 < (datetime.datetime.now().date() - all_item.created.date()).days <= 6:
                all_days3 += 1
            elif (datetime.datetime.now().date() - all_item.created.date()).days >= 7:
                all_days7 += 1

            if all_item.assigned==None:
                all_unassigned+=1

        all = {'all_total': all_total, 'all_fresh': all_fresh, 'all_cancelled': all_cancelled, 'all_closed': all_closed,
               'all_rescheduled': all_rescheduled, 'all_follow_up': all_follow_up, 'all_acknowledged': all_acknowledged,
               'all_pending_cancelled': all_pending_cancelled, 'all_days7': all_days7, 'all_days3': all_days3,'all_unassigned':all_unassigned}

        names = User.objects.order_by('username').values('username').distinct()
        report_name = []
        final = {}
        for item in names:
            one = item['username']
            report_name.append(one)
            cursor = connection.cursor()
            cursor.execute('select id from auth_user where username = "' + one + '"')
            assigned_id = cursor.fetchall()
            tot = 0
            fresh = 0
            cancelled = 0
            closed = 0
            other = 0
            rescheduled = 0
            follow_up = 0
            acknowledged = 0
            pending_cancelled = 0
            days3 = 0
            days7 = 0


            user_data = models.Final.objects.raw(
                'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and assigned_id ="' + str(
                    assigned_id[0][0]) + '" ')
            for count in user_data:
                tot += 1
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
                elif count.status == 'acknowledged':
                    acknowledged += 1
                elif count.status == 'pending_cancelled':
                    pending_cancelled += 1
                else:
                    other += 1

                if 3 < (datetime.datetime.now().date() - count.created.date()).days <= 6:
                    days3 += 1
                elif (datetime.datetime.now().date() - count.created.date()).days >= 7:
                    days7 += 1


            final[f'{one}'] = {'tot': tot, 'fresh': fresh, 'cancelled': cancelled, 'closed': closed,
                               'rescheduled': rescheduled, 'follow_up': follow_up, 'other': other,
                               'acknowledged': acknowledged, 'pending_cancelled': pending_cancelled, 'days3': days3,
                               'days7': days7,'assigned_id':assigned_id[0][0]}

        return render(request, 'report.html', {'all': all, 'final': final, 'user_data': user_data})
    else:
        all_data = models.Final.objects.raw('select * from accounts_final')
        return render(request, 'report.html', {'all_data': all_data})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(
        ['Lead Id', 'Name', 'Number', 'Email', 'City', 'State', 'Link Of Cancellation', 'Weight', 'Height', 'BMI',
         'Gender', 'Contact', 'Type', 'Created'
            , 'Rescheduled', 'Comment', 'Status', 'Substatus', 'Assigned User ID', 'Assigned Username', 'Lead age',
         'Range'])
    if request.user.is_staff:

        for member in models.Final.objects.all().values_list('id', 'name', 'number', 'email', 'city', 'state',
                                                             'insta_user', 'weight',
                                                             'height', 'bmi', 'gender', 'contact', 'type', 'created'
                , 'rescheduled', 'comment', 'status', 'substatus', 'assigned'):
            i = member[-1]
            created = member[13]
            print(created)

            try:
                name = User.objects.filter(id=i)[0]
            except:
                name = 'None'
            range = ''
            days = (datetime.datetime.now().date() - created.date()).days
            if days < 3:
                range = '0-2'
            elif 3 < days < 7:
                range = '3-6'
            else:
                range = '+7'

            new = member + (name, days, range)
            writer.writerow(new)
    else:
        u = request.user
        for member in models.Final.objects.all().filter(assigned=u).values_list('id', 'name', 'number', 'email', 'city',
                                                                                'state', 'insta_user', 'weight',
                                                                                'height', 'bmi', 'gender', 'contact',
                                                                                'type', 'created'
                , 'rescheduled', 'comment', 'status', 'substatus', 'assigned'):
            created = member[13]
            name = User.objects.filter(id=request.user.id)[0]

            range = ''
            days = (datetime.datetime.now().date() - created.date()).days
            if days < 3:
                range = '0-2'
            elif 3 <= days < 7:
                range = '3-6'
            else:
                range = '+7'

            new = member + (name, days, range)

            writer.writerow(new)

    response['Content-Disposition'] = 'attachement; filename="Wefit.csv"'
    '''models.Final.objects.all().values_list('name','number','email','city','state','weight','height','bmi','gender','contact','type','created'
                     ,'rescheduled','comment','status','substatus','assigned')'''
    return response
