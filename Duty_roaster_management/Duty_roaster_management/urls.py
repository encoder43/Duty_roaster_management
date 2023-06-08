"""Duty_roaster_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ShiftEase.views import *
from ShiftEase import views
from django.views.generic.edit import UpdateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('registration', registration, name='registration'),
    path('emp_login', emp_login, name='emp_login'),
    path('emp_home', emp_home, name='emp_home'),
    path('view_profile/', view_profile, name='view_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),
    path('logout/', emp_logout, name='logout'),
    path('sup_login/', sup_login, name='sup_login'),
    path('sup_home/', sup_home, name='sup_home'),
    #Company paths
    path('comp', views.comp),
    path('show', views.show),
    path('edit/<str:cName>', views.edit),
    path('update/<str:cName>', views.update),
    path('delete/<str:cName>', views.delete),


    path('emp/', views.emp),
    path('updateEmp/<str:eFname>/', views.updateEmp),
    path('showemp/', views.showemp, name='showemp'),
    path("deleteemployee/", deleteemployee, name="deleteemployee"),
    path('editemployee/', UpdateView.as_view(), name='editemployee'),
    path('helpdesk/', HelpdeskView.as_view(), name='helpdesk'),
    path('', views.index, name='index'),
    path('send_message/', views.send_message, name='send_message'),
    path("shift-change-request/", shift_change_request, name="shift_change_request"),
    path('submit_leave_request/', submit_leave_request, name='submit_leave_request'),
    path('sup_home/assign_duties/', assign_duties_view, name='assign_duties'),
    path('view-duties/', views.view_duties_view, name='view_duties'),

]
