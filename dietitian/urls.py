from django.urls import path

from . import views

urlpatterns = [
    path('clients', views.clients, name="clients"),
    path('client_register',views.client_register,name='client_register'),
    path('client_token',views.client_token,name='client_token'),
    path('client_edit',views.client_edit,name='client_edit'),
    path('dashboard',views.dietitian_dashboard,name='dietitian_dashboard')
               ]