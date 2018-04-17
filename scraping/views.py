from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
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

def get_all_specialty_in_each_city():
    """ 
    Построение словаря по данным всех подписчиков, 
    где ключ - id города, а значение - 
    список id специальностей, которые необходимо искать в этом городе 
    """
    cities_qs = Subscriber.objects.all().values('city')
    cities_id = set([i['city'] for i in cities_qs])
    cities = City.objects.filter(pk__in=cities_id)
    # print(cities)
    all_ = {}
    for city in cities:
        specialty_qs = Subscriber.objects.filter(city=city.id)
        tmp = set()
        for sp in specialty_qs:
            tmp.add(sp.specialty.id)
            # print(tmp)
        all_[city.id] = set(tmp)
    
    return all_
    
    
def get_urls(cities):
    """
    Возвращает список с url-адресами, для каждого города и специальности, 
    из входящего словаря 
    """
    all_urls = []
    tmp_city = {}
    for city in cities:
        for sp in cities[city]:
            tmp = {}
            qs = Url.objects.filter(city=city, specialty=sp)
            tmp['city'] = city
            tmp['specialty'] = sp
            for item in qs:
                tmp[item.site.name] = item.address
            all_urls.append(tmp)
    return all_urls     


def scraping_sites():
    """
    Согласно данных от подписчиков, формируются задачи для поиска - 
    в каких городах, какие специальности искать. По результатам скрапинга, 
    возвращает список с данными, полученными с сайтов по каждому 
    городу и специальности
    """
    todo_list = get_all_specialty_in_each_city()
    url_list = get_urls(todo_list)
    jobs = []
    for url in url_list:
        tmp = {}
        tmp_content = []
        tmp_content.extend( djinni(url['Djinni.co']))
        tmp_content.extend( work(url['Work.ua']))
        tmp_content.extend( rabota(url['Rabota.ua']))
        tmp_content.extend( dou(url['Dou.ua']))
        tmp['city'] = url['city']
        tmp['specialty'] = url['specialty']
        tmp['content'] = tmp_content
        jobs.append(tmp)
    return jobs


def save_to_db(request):
    """
    Получает информацию по результату скрапинга и сохраняет её в БД
    Дополнительно информация проверяется на уникальность, 
    чтобы не было дубликатов с одного и того же сайта.
    """
    all_data = scraping_sites()
    for data in all_data:
        city = City.objects.get(id=data['city'])
        specialty = Specialty.objects.get(id=data['specialty'])
        jobs = data['content']
        jobs.reverse()
        for job in jobs:
            vacancy = Vacancy(city=city, specialty=specialty,
                                title=job['title'], url=job['href'],
                                description=job['descript'],
                                company=job['company'])
            try:
                vacancy.save()
            except IntegrityError:
                pass
        
    return render(request, 'scraping/home.html', {'jobs': jobs})
    
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