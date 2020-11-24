from django.urls import path

from . import views

urlpatterns = [
	path('',views.register,name='register'),
	path('register', views.register, name="store"),
	path('manager',views.show,name="show"),
	path("show_saurabh",views.show_saurabh,name="show Saurabh"),
	path('token',views.token,name="token"),
	path('show_vikas',views.show_vikas,name='show vikas'),
	path('show_userone',views.show_userone,name='show userone'),
	path('show_usertwo',views.show_usertwo,name='show usertwo'),
	path('show_userthree',views.show_userthree,name='show userthree'),
]