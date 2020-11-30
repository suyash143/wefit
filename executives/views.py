import os, sys
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from accounts.models import Final
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts import add_admin_use


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

def employee_add(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
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
                    count= 0
                    all_users=User.objects.all()
                    for users in all_users:
                        count+=1
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
            return redirect('/all')
        else:
            messages.info(request,"invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


