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
from django.conf.urls import url
from django.contrib import admin
from scraping.views import send_emails_to_all_subscribers, save_to_db
from subscribers import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^send/$', send_emails_to_all_subscribers, name='send'),
    url(r'^job/$', save_to_db, name='scraping'),
    url(r'update/$', views.update_subscriber, name='update'),
    url(r'^login/$', views.login_subscriber, name='login'),
    url(r'^', views.SubscriberCreate.as_view(), name='home'),
]
