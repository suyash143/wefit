from django.urls import path

from . import views

urlpatterns = [
	path('register', views.register, name="store"),
	path('',views.show,name="show"),
	path("show_saurabh",views.show_saurabh,name="show Saurabh")
]