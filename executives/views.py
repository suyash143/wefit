import os, sys
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from accounts.models import Final,Questions,Info,Record
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts import add_admin_use
from django.http import HttpResponse
import datetime


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

def employee_add(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        number=request.POST['number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if len(password1)<8:
            messages.info(request,"Password Should be Atleast 8 character long")
            return render(request,'employee_add.html')
        else:
            if password1==password2:
                if User.objects.filter(username=username):
                    messages.info(request,'Username Taken')
                    return render(request,'employee_add.html')

                elif User.objects.filter(email=email):
                    messages.info(request,'Email Taken')
                    return render(request,'employee_add.html')
                else:
                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user.save()
                    user.info.mobile=number
                    user.save()

                    count= 0
                    all_users=User.objects.latest('pk')
                    id = all_users.pk
                    count=id
                    user_str=str(username)
                    count_str=str(count)
                    add_admin_use.user_adder(user_str)
                    add_admin_use.admin_body(user_str,count_str)




                    print('user created')

                    return redirect('login')

            else:
                messages.info(request,'passoword incorrect')
                return render(request,'employee_add.html')
    else:
        return render(request,'employee_add.html')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            if request.user.info.is_dietitian is True:
                return redirect('/dietitian/dashboard')
            else:
                return redirect('/dashboard')
        else:
            messages.info(request,"invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')


def logout(request):
    auth.logout(request)
    latest = User.objects.latest('pk')

    id=latest.pk

    return redirect('login')


def employee(request):
    if request.user.is_staff:
        names=User.objects.filter(is_staff=0)
        if request.method=="POST":
            employee_id=request.POST['employee_id']
            request.session['employee_id'] = employee_id
            print(employee_id)
            return redirect('employee_profile')
        return render(request,'employee_manage.html',{'names':names})
    else:
        return HttpResponse("You Do Not Have permission ")

def employee_profile(request):
    if request.user.is_staff:
        employee_id=request.session['employee_id']
        name=User.objects.get(pk=employee_id)
        if request.method=="POST":
            emp_id=request.POST["employee_pk"]
            print(emp_id,employee_id)
            start_date = name.info.date_start
            end_date = name.info.date_end
            today = datetime.date.today()
            next_monday = today - datetime.timedelta(days=today.weekday())
            next_6 = next_monday + datetime.timedelta(days=6)
            target = name.info.target
            achieved = name.info.target_achieved

            mod, created = Record.objects.get_or_create(start_date=start_date, end_date=end_date, target=target,
                                                               achieved=achieved, user_id=name.pk,username=name.username)
            mod.save()
            add_admin_use.user_delete(str(name.username),name.pk)
            name.delete()

            return redirect('employee')
        return render(request,'employee_profile.html',{'name':name})
    else:
        return HttpResponse("you Do Not have Permission")