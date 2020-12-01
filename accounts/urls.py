from django.urls import path

from . import views

urlpatterns = [
	path('',views.register,name='register'),
	path('register', views.register, name="store"),
	path('token',views.token,name="token"),

	path('all',views.all,name='all'),
	path('edit_employee',views.edit_employee,name='edit_employee'),
	path('report',views.report,name='Report')
]