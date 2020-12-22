from django.urls import path

from . import views

urlpatterns = [
	path('',views.register,name='register'),
	path('register', views.register, name="store"),
	path('token',views.token,name="token"),

	path('all',views.all,name='all'),
	path('edit_employee',views.edit_employee,name='edit_employee'),
	path('report',views.report,name='Report'),
	path('download',views.export_csv,name='csv'),
	path('dashboard',views.dashboard,name='dashboard'),
	path('profile',views.profile,name='profile'),
	path('target',views.target,name='target'),
	path('info_edit',views.info_edit,name='info_edit'),
	path('target_reset',views.target_reset,name='target_reset'),
	path('follow_up',views.follow_up,name='follow_up')
]