from django.shortcuts import render
import datetime

from .models import *
from subscribers.models import *
from .utils import *

TWO_DAYS_AGO = datetime.date.today()-datetime.timedelta(2)


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
