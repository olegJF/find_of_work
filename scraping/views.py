from django.shortcuts import render
from django.http import HttpResponse

import datetime

from .models import *
from subscribers.models import *
from .utils import *
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

WEEK_AGO = datetime.date.today()-datetime.timedelta(7)
ONE_DAY_AGO = datetime.date.today()-datetime.timedelta(1)
SUBJECT = 'Vacancy list'
FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


    
def delete_old_records():
    Vacancy.objects.filter(timestamp__lt=WEEK_AGO).delete()
    return True


def get_set_of_all_cities_and_specialties():
    """ 
    Построение множества кортежей по данным всех подписчиков, 
    с парами id города и id специальности 
    """
    qs = Subscriber.objects.all().values('city', 'specialty')
    data = set([(i['city'], i['specialty']) for i in qs])
    return data
    
    
def send_emails_to_all_subscribers(request):
    data_of_requests = get_set_of_all_cities_and_specialties()
    for pair in data_of_requests:
        template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
        end = '</body></html>'
        content = ''
        city = City.objects.get(id=pair[0])
        specialty = Specialty.objects.get(id=pair[1])
        email_qs = Subscriber.objects.all().filter(city=city, 
                                            specialty=specialty).values('email')
        emails = [i['email'] for i in email_qs]
        jobs_qs = Vacancy.objects.filter(city=city, specialty=specialty,
                                    timestamp=datetime.date.today())
        for job in jobs_qs:
            content += '<a href="{}" target="_blank">'.format(job.url)
            content += '{}</a>'.format(job.title)
            content += '<br/><p>{}</p><br/>'.format(job.description)
            content += '<hr><br/>'
        template = template + content + end
        for email in emails:
            recipient_list = [email]
            text_content = 'This is an important message.'
            msg = EmailMultiAlternatives(SUBJECT, text_content, FROM_EMAIL, recipient_list)
            msg.attach_alternative(template, "text/html")
            msg.send()
    return HttpResponse( '<h1>God!</h1>')