"""vacancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.urls import re_path, path
from django.contrib import admin
from scraping.views import *
from subscribers import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^update/$', views.update_subscriber, name='update'),
    re_path(r'^login/$', views.login_subscriber, name='login'),
    re_path(r'^contact/$', views.contact_admin, name='contact'),
    re_path(r'^list/', vacancy_list, name='list'),
    re_path(r'^subscribe/$', views.SubscriberCreate.as_view(), name='subscribe'),
    path('', home, name='home'),
    # url(r'^', home, name='home'),
    
]
