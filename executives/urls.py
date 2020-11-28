from django.urls import path

from . import views

urlpatterns =[
    path('register',views.employee_add,name='register'),
    path('',views.login,name='login'),
    path('login',views.login,name='login')
    ]