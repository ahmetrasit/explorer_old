"""explorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""

from django.conf.urls import include, url
from django.contrib import admin
from manager import views as manager_views
from django.contrib.auth import views as auth_views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', manager_views.homepage, name='homepage'),
    url(r'^config/main$', manager_views.editMainConfiguration, name='editMainConfiguration'),
    url(r'^add/user$', manager_views.addUser, name='addUser'),
    url(r'^add/dataCategory$', manager_views.addDataCategory, name='addDataCategory'),
    url(r'^add/step$', manager_views.createStep, name='createStep'),
    url(r'^add/reference$', manager_views.addReference, name='addReference'),
    url(r'^new/step/$', manager_views.addStep, name='addStep'),
    url(r'^get/data_points/$', manager_views.getAllDataPoints, name='getAllDataPoints'),


    url(r'^login/$', auth_views.login, {'template_name': 'homepage.html'}),
    url(r'^upload/$', manager_views.upload, name='upload'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]
