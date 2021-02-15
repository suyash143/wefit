from django.urls import path

from . import views
from accounts.views import report,export_csv
urlpatterns =[
    path('register',views.employee_add,name='register'),
    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    path('report',report,name="report"),
    path('download',export_csv,name='download'),
    path('employee',views.employee,name='employee'),
    path('employee_profile',views.employee_profile,name='employee_profile'),
    path('dietitian_add',views.dietitian_add,name='dietitian_add')

    ]
