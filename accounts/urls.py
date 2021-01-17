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
	path('follow_up',views.follow_up,name='follow_up'),
	path('dashboard_register',views.register_emp,name='dashboard_register'),
	path('dashboard_script',views.dashboard_script,name='dashboard_script'),
	path('dashboard_script_edit',views.dashboard_script_edit,name='dashboard_script_edit'),
	path('dashboard_script_add',views.dashboard_script_add,name='dashboard_script_add'),
	path('dashboard_log',views.get_current_users,name='dashboard_log'),
	path('delete_session',views.delete_session,name='delete_session'),
	path('create_information',views.create_information,name='create_information')
]