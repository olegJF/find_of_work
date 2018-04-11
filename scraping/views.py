from django.shortcuts import render
import datetime

from .models import *
from subscribers.models import *
from .utils import *

TWO_DAYS_AGO = datetime.date.today()-datetime.timedelta(2)

def get_all_specialty_in_each_city():
    """ Построение словаря по данным всех подписчиков, 
    где ключ - id города, а значение - 
    список специальностей, которые необходимо искать в этом городе """
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
    """Создание списка с url-адресами, для каждого города и специальности, 
    из входящего словаря """
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
    todo_list = get_all_specialty_in_each_city()
    url_list = get_urls(todo_list)
    jobs = []
    for url in url_list:
        tmp = {}
        tmp_content = []
        tmp_content.extend( djinni(url['Djinni.co']))
        # tmp_content.extend( work(url['Work.ua']))
        # tmp_content.extend( rabota(url['Rabota.ua']))
        # tmp_content.extend( dou(url['Dou.ua']))
        tmp['city'] = url['city']
        tmp['specialty'] = url['specialty']
        tmp['content'] = tmp_content
        jobs.append(tmp)
    return jobs

def save_to_db(request):
    all_data = scraping_sites()
    vacancy = Vacancy.objects.filter(timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    for data in all_data:
        city = City.objects.get(id=data['city'])
        specialty = Specialty.objects.get(id=data['specialty'])
        jobs = data['content']
        for job in jobs:
            if job['href'] not in vacancy_url_list:
                vacancy = Vacancy(city=city, specialty=specialty,
                                title=job['title'], url=job['href'],
                                description=job['descript'],
                                company=job['company'])
                vacancy.save()
        
    return render(request, 'scraping/home.html', {'jobs': jobs})

def djinni_scraping(request):
    subscriber = Subscriber.objects.all().first()
    site = Site.objects.all().filter(name='Djinni.co').first()
    url = Url.objects.get(city=subscriber.city, specialty=subscriber.specialty,
                            site=site)
    vacancy = Vacancy.objects.filter(city=subscriber.city,
                                    specialty=subscriber.specialty, site=site,
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = djinni(url.address)
    # print(str(vacancy_url_list).encode('utf-8'))
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=subscriber.city,
                            specialty=subscriber.specialty, site=site,
                            title=job['title'], url=job['href'],
                            description=job['descript'],
                            company=job['company'])
            vacancy.save()
    return render(request, 'scraping/home.html', {'jobs': jobs})


def work_scraping(request):
    site = Site.objects.all().filter(name='Work.ua').first()
    subscriber = Subscriber.objects.all().first()
    url = Url.objects.get(city=subscriber.city, specialty=subscriber.specialty,
                            site=site)
    vacancy = Vacancy.objects.filter(city=subscriber.city,
                                    specialty=subscriber.specialty, site=site,
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = work(url.address)
    # print(city, specialty, site, url.address)

    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=subscriber.city,
                            specialty=subscriber.specialty, site=site,
                            title=job['title'], url=job['href'],
                            description=job['descript'],
                            company=job['company'])
            vacancy.save()
    return render(request, 'scraping/home.html', {'jobs': jobs})


def rabota_scraping(request):
    site = Site.objects.all().filter(name='Rabota.ua').first()
    subscriber = Subscriber.objects.all().first()
    url = Url.objects.get(city=subscriber.city, specialty=subscriber.specialty,
                            site=site)
    vacancy = Vacancy.objects.filter(city=subscriber.city,
                                    specialty=subscriber.specialty, site=site,
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = rabota(url.address)
    # print(city, specialty, site, url.address)
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=subscriber.city,
                            specialty=subscriber.specialty, site=site,
                            title=job['title'], url=job['href'],
                            description=job['descript'],
                            company=job['company'])
            vacancy.save()
    return render(request, 'scraping/home.html', {'jobs': jobs})


def dou_scraping(request):
    site = Site.objects.all().filter(name='Dou.ua').first()
    print(site)
    subscriber = Subscriber.objects.all().first()
    url = Url.objects.get(city=subscriber.city, specialty=subscriber.specialty,
                            site=site)
    vacancy = Vacancy.objects.filter(city=subscriber.city,
                                    specialty=subscriber.specialty, site=site,
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = dou(url.address)
    # print(city, specialty, site, url.address)
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=subscriber.city,
                            specialty=subscriber.specialty, site=site,
                            title=job['title'], url=job['href'],
                            description=job['descript'],
                            company=job['company'])
            vacancy.save()
    return render(request, 'scraping/home.html', {'jobs': jobs})
