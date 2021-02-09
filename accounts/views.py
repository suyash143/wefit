import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from .models import Final
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
import pytz
from django.contrib.sessions.models import Session


from datetime import date
from django.utils import timezone
from django.db import connection
import datetime
from . import utils
from django.core.paginator import Paginator
from django.conf import settings
from django.core.mail import send_mail

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
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
        # Query all logged in users based on id list
        active_user=User.objects.filter(id__in=user_id_list,is_staff=0)
        active_user_count=active_user.count()

        c = open(os.path.join(BASE, 'employee.txt', ))
        count = c.readline()
        num = count.partition(' ')[0]
        c.close()
        if int(num) >= active_user_count != 0:
            writer = open(os.path.join(BASE, 'employee.txt'), 'w+')
            writer.write(str(0))
            writer.close()
            c = open(os.path.join(BASE, 'employee.txt', ))
            count = c.readline()
            num = count.partition(' ')[0]
            c.close()
            lead3, created = models.Final.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                                state=state, weight=weight,
                                                                height=height, gender=gender,

                                                                contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                                created=datetime.datetime.now(), status='fresh',assigned=active_user[int(num)])
            lead3.save()

        elif int(num)<int(active_user_count) and active_user_count !=0:
            lead3, created = models.Final.objects.get_or_create(name=name, email=email, number=number, city=city,
                                                            state=state, weight=weight,
                                                            height=height, gender=gender,

                                                            contact=mode, type=goal, insta_user=instauser, bmi=bmi,
                                                            created=datetime.datetime.now(), status='fresh',assigned=active_user[int(num)])
            lead3.save()
            c = open(os.path.join(BASE, 'employee.txt'))
            count = c.readline()
            c.close()
            writer = open(os.path.join(BASE, 'employee.txt'), 'w+')
            writer.write(str(int(count) + 1))
            writer.close()


        else:
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

            name = models.Final.objects.all().order_by('-created')
            name_paginator=Paginator(name,130)
            page_num=request.GET.get('page')
            page=name_paginator.get_page(page_num)

        else:
            name = models.Final.objects.all().filter(assigned=user).order_by('-created')
            name_paginator = Paginator(name, 130)
            page_num = request.GET.get('page')
            page = name_paginator.get_page(page_num)

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

                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)

                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": fresh, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})

                elif filter_value == "closed":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": closed, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})
                elif filter_value == "rescheduled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': rescheduled, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': 0,'page':page})
                elif filter_value == "cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": cancelled, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})
                elif filter_value == "follow_up":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'page':page,'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': follow_up, 'acknowledged': 0, 'pending_cancelled': 0})

                elif filter_value == "acknowledged":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': acknowledged,
                                   'pending_cancelled': 0,'page':page})

                elif filter_value == "pending_cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': pending_cancelled,'page':page})
                else:
                    name = models.Final.objects.raw(
                        'select * from accounts_final where created between "' + startdate + '" and "' + todate + '"')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other,
                               'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                               'pending_cancelled': pending_cancelled,'page':page}
                    return render(request, 'dashboard_lead.html', context)
            else:
                if filter_value == "fresh":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": fresh, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})

                elif filter_value == "closed":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": closed, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})
                elif filter_value == "rescheduled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': rescheduled, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': 0,'page':page})
                elif filter_value == "cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": cancelled, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0, 'pending_cancelled': 0,
                                   'page':page})
                elif filter_value == "follow_up":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': follow_up, 'acknowledged': 0, 'pending_cancelled': 0,'page':page})

                elif filter_value == "acknowledged":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': acknowledged,
                                   'pending_cancelled': 0,'page':page})

                elif filter_value == "pending_cancelled":
                    name = models.Final.objects.raw(
                        'select * from accounts_final where (created between "' + startdate + '" and "' + todate + '") and status ="' + filter_value + '" and assigned_id="' + str(
                            user_id) + '" ')
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    return render(request, 'dashboard_lead.html',
                                  {'name': name, "fresh": 0, "cancelled": 0, "closed": 0, "other": other,
                                   'rescheduled': 0, 'follow_up': 0, 'acknowledged': 0,
                                   'pending_cancelled': pending_cancelled,'page':page})

                else:
                    name = models.Final.objects.all().filter(assigned=user)
                    name_paginator = Paginator(name, 100)
                    page_num = request.GET.get('page')
                    page = name_paginator.get_page(page_num)
                    context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other,
                               'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                               'pending_cancelled': pending_cancelled,'page':page}

                    return render(request, 'dashboard_lead.html', context)

        context = {'name': name, "fresh": fresh, "cancelled": cancelled, "closed": closed, "other": other, 'al': al,
                   'rescheduled': rescheduled, 'follow_up': follow_up, 'acknowledged': acknowledged,
                   'pending_cancelled': pending_cancelled, 'unassigned': unassigned,'page':page}

        return render(request, 'dashboard_lead.html', context)
    else:
        return HttpResponse('<h1>Forbidden</h1><h2>Please Log in to view your data</h2>')


def edit_employee(request):
    id = request.session.get('id')
    name = models.Final.objects.get(id=id)
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
        total= request.POST.get('total',0)
        paid=request.POST.get('paid',0)
        updater.status = status
        updater.substatus = substatus
        updater.insta_user = cancel_link
        updater.comment = comment
        updater.rescheduled = rescheduled



        updater.save()
        if updater.status=='closed':
            updater.purchased=total
            if updater.paid is None:
                updater.paid=paid
                updater.save()
                assigned=updater.assigned.pk
                target_updater=models.Info.objects.get(user_id=assigned)

                target_updater.target_achieved=int(target_updater.target_achieved)+int(paid)
                target_updater.save()
            else:
                previous_paid=updater.paid
                updater.paid=paid
                money_acquired=abs(int(paid)-int(previous_paid))
                updater.save()
                assigned=updater.assigned.pk
                target_updater=models.Info.objects.get(user_id=assigned)
                target_updater.target_achieved=int(target_updater.target_achieved)+int(money_acquired)
                target_updater.save()



        return redirect('all')
    return render(request, 'dashboard_edit_employee.html',
                  {'id': id,  'name': name,
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

        names = User.objects.filter(is_staff=0).order_by('username').values('username').distinct()
        print(names)

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

        return render(request, 'dashboard_report.html', {'all': all, 'final': final, 'user_data': user_data})
    else:
        all_data = models.Final.objects.raw('select * from accounts_final')
        return render(request, 'dashboard_report.html', {'all_data': all_data})


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


def dashboard(request):
    if request.user.is_authenticated:
        today=datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        next_6 = monday + datetime.timedelta(days=6)
        id=request.user.id
        today_data = models.Final.objects.raw(
            'select * from accounts_final where (created like "%' + str(today) + '%" ) and assigned_id ="' + str(id) + '" ')
        week_data=user_data = models.Final.objects.raw(
                'select * from accounts_final where (created between "' + str(monday) + '" and "' + str(next_6) + '") and assigned_id ="' + str(id) + '" ')
        tot=models.Final.objects.filter(assigned=request.user,created__date=today).count()
        fresh = models.Final.objects.filter(assigned=request.user,created__date=today,status='fresh').count()
        follow_up = models.Final.objects.filter(assigned=request.user, status='follow_up',created__date=today).count()
        pending_cancelled = models.Final.objects.filter(assigned=request.user, status='pending_cancelled', created__date=today).count()
        closed = models.Final.objects.filter(assigned=request.user, status='closed', created__date=today).count()
        acknowledged=models.Final.objects.filter(assigned=request.user, status='acknowledged', created__date=today).count()

        this_day={'tot':tot,'fresh':fresh,'follow_up':follow_up,'pending_cancelled':pending_cancelled,'closed':closed,'acknowledged':acknowledged}

        man_tot = models.Final.objects.filter(created__date=today).count()
        man_fresh = models.Final.objects.filter(created__date=today, status='fresh').count()
        man_follow_up = models.Final.objects.filter(status='follow_up', created__date=today).count()
        man_pending_cancelled = models.Final.objects.filter(status='pending_cancelled',
                                                        created__date=today).count()
        man_closed = models.Final.objects.filter(status='closed', created__date=today).count()
        man_acknowledged = models.Final.objects.filter(status='acknowledged',
                                                   created__date=today).count()
        man={'man_tot':man_tot,'man_fresh':man_fresh,'man_follow_up':man_follow_up,'man_pending_cancelled':man_pending_cancelled,'man_closed':man_closed,
            'man_acknowledged':man_acknowledged}
        week_assigned=0
        week_cancelled=0
        week_closed=0
        for items in week_data:
            week_assigned+=1
            if items.status=="closed":
                week_closed+=1
            elif items.status=="cancelled":
                week_cancelled+=1
            else:
                pass

        names = User.objects.filter(is_staff=0).order_by('username').distinct()

        try:
            remaining=abs(request.user.info.target-request.user.info.target_achieved)


        except:
            remaining = request.user.info.target
            percent = (remaining / request.user.info.target) * 100

        total_target=0
        total_target_achieved=0
        total_target_remaining=0
        for objs in names:
            total_target+=objs.info.target
            total_target_achieved+=objs.info.target_achieved
        total_target_remaining=abs(total_target-total_target_achieved)

        return render(request,'dashboard.html',{'week_assigned':week_assigned,'week_cancelled':week_cancelled,'week_closed':week_closed,'total_target':total_target,'total_target_achieved':total_target_achieved,
                                                'total_target_remaining':total_target_remaining,'names':names,'remaining':remaining,'today':today,'this_day':this_day,'man':man})
    else:
        return HttpResponse('Please Log In to View Your Data')

def profile(request):
    return render(request,'profile.html')


def target(request):
    users=User.objects.all().filter(is_staff=0)
    if request.method == "POST" and 'id' in request.POST:
        id = request.POST.get('id')

        request.session['user_id'] = id

        return redirect('info_edit')
    return render(request,'target.html',{'users':users})

def info_edit(request):
    pk = request.session.get('user_id')
    users=User.objects.get(pk=pk)
    if request.method=='POST':
        target=request.POST.get('target')
        mobile=request.POST.get('mobile')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        users.info.target=target
        users.save()
    return render(request,'edit_info.html',{'users':users})




def target_reset(request):
    if request.user.is_staff:
        first=User.objects.filter(is_staff=0)[0]
        start_date=first.info.date_start
        end_date = first.info.date_end
        today=datetime.date.today()
        next_monday=today-datetime.timedelta(days=today.weekday())
        next_6=next_monday+datetime.timedelta(days=6)
        target_saver=User.objects.filter(is_staff=0)
        for item in target_saver:
            id=item.pk
            target=item.info.target
            achieved=item.info.target_achieved
            username=item.username

            mod, created = models.Record.objects.get_or_create(start_date=start_date,end_date=end_date,target=target,achieved=achieved,user_id=id,username=username)
            mod.save()
            changer=item.info
            changer.target=target
            changer.target_achieved=0
            changer.date_start=next_monday
            changer.date_end=next_6
            changer.save()

        return redirect('target')
    else:
        return HttpResponse("you do not have permission")


def email_sender():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    all_data = models.Final.objects.raw(
        'select * from accounts_final where created between "' + str(yesterday) + '" and "' + str(today) + '"')
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

        if all_item.assigned == None:
            all_unassigned += 1
    message=f'Todays total Leads:{all_total} ,Fresh: {all_fresh} , Follow Up: {all_follow_up}, Acknowledged: {all_acknowledged}, Cancelled:{all_cancelled},  Acknowledged: {all_acknowledged}' \
            f'Pending To be Cancelled :{all_pending_cancelled}  Unassigned: {all_unassigned} '
    
    names = User.objects.filter(is_staff=0).order_by('username').distinct()
    for item in names:
        message+=f'{item.username} Target:{item.info.target} Achieved: {item.info.target_achieved}'

        id=item.pk
        data = models.Final.objects.raw(
            'select * from accounts_final where (created like "%' + str(today) + '%" ) and assigned_id ="' + str(
                id) + '" ')

    subject = 'Wefit Daily Report'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['suyashpathak143@gmail.com']
    send_mail(subject, message, email_from, recipient_list)





def follow_up(request):
    if request.user.is_authenticated:
        today = datetime.date.today()
        id = request.user.id
        rescheduled_data = models.Final.objects.raw(
            'select * from accounts_final where (rescheduled like "%' + str(today) + '%" ) and assigned_id ="' + str(
                id) + '" ')

        name_paginator = Paginator(rescheduled_data, 100)
        page_num = request.GET.get('page')
        page = name_paginator.get_page(page_num)
        return render(request,'dashboard_follow_up.html',{'rescheduled_data':rescheduled_data,'page':page})

def register_emp(request):
    if request.method=='POST':

        name = request.POST['name']
        number = request.POST['number']

        weight = request.POST['weight']
        foot = request.POST.get('foot', 5)
        inch = request.POST.get('inch', 8)
        gender = request.POST['gender']

        height = (((float(foot) * 12) + float(inch)) * 2.54) / 100
        bmi = float(weight) / (height * height)

        IST = pytz.timezone('Asia/Kolkata')

        if models.Final.objects.filter(number=number).order_by('-id')[:100]:
            return redirect('/token')

        lead3, created = models.Final.objects.get_or_create(name=name, number=number, weight=weight,
                                                            height=height, gender=gender,bmi=bmi,
                                                            created=datetime.datetime.now(), status='fresh',assigned=request.user)
        lead3.save()

        return redirect("/all ")

    else:
        return render(request,"dashboard_register.html")


def dashboard_script(request):
    script=models.Questions.objects.all()
    category=models.Questions.objects.values('category').distinct()
    if request.method=="POST" and 'script_id' in request.POST:
        script_id=request.POST['script_id']
        request.session['script_id']=script_id
        return redirect('dashboard_script_edit')

    elif request.method=='POST' and 'filter' in request.POST:
        filter_value=request.POST['filter']
        script=models.Questions.objects.filter(category=filter_value)
        return render(request,'dashboard_script.html',{'script':script,'category':category})
    return render(request,'dashboard_script.html',{'script':script,'category':category})

def dashboard_script_edit(request):
    script_id=request.session['script_id']
    print(script_id)
    if script_id:
        script=models.Questions.objects.all().get(pk=script_id)
        if request.method=='POST':

            category = request.POST['category']
            question = request.POST['question']
            answer = request.POST['answer']
            script.category=category
            script.questions=question
            script.answers=answer
            script.save()
        return render(request, "dashboard_script_edit.html", {'script': script})

    return render(request,"dashboard_script_edit.html")

def dashboard_script_delete(request):
    script_id = request.session['script_id']
    obj=models.Questions.objects.get(pk=script_id)
    obj.delete()
    return redirect('dashboard_script')


def dashboard_script_add(request):

    if request.method == 'POST':
        category = request.POST['category']
        question = request.POST['question']
        answer = request.POST['answer']
        sc, created = models.Questions.objects.get_or_create(category=category,questions=question,answers=answer)
        sc.save()

    return render(request,"dashboard_script_edit.html")



def get_current_users(request):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    print(User.objects.filter(id__in=user_id_list,is_staff=0).count())
    all_users=User.objects.all()
    users=User.objects.filter(id__in=user_id_list,is_staff=0)

    return render(request, 'dashboard_logs.html', {'users':users,'all_users':all_users})


def delete_session(request):
    request.session.flush()
    request.session.clear_expired()
    return render(request,'blank.html')


