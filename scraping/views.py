from django.shortcuts import render
import datetime

from .models import *
from .utils import *

TWO_DAYS_AGO = datetime.date.today()-datetime.timedelta(2)

def djinni_scraping(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    site = Site.objects.get(name='Djinni.co')
    url = Url.objects.get(city=city, specialty=specialty, site=site)
    vacancy = Vacancy.objects.filter(city=city, specialty=specialty, site=site, 
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = djinni(url.address)
    # print(str(vacancy_url_list).encode('utf-8'))
    
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=city, specialty=specialty, site=site,
                                title=job['title'] , url=job['href'], 
                                description=job['descript'], 
                                company=job['company'])
            vacancy.save()
        
    
    return render(request, 'scraping/home.html', {'jobs': jobs})

def work_scraping(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    site = Site.objects.get(name='Work.ua')
    url = Url.objects.get(city=city, specialty=specialty, site=site)
    vacancy = Vacancy.objects.filter(city=city, specialty=specialty, site=site, 
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = work(url.address)
    # print(city, specialty, site, url.address)
    
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=city, specialty=specialty, site=site,
                                title=job['title'] , url=job['href'], 
                                description=job['descript'], 
                                company=job['company'])
            vacancy.save()
        
    
    return render(request, 'scraping/home.html', {'jobs': jobs})
    
def rabota_scraping(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    site = Site.objects.get(name='Rabota.ua')
    url = Url.objects.get(city=city, specialty=specialty, site=site)
    vacancy = Vacancy.objects.filter(city=city, specialty=specialty, site=site, 
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = rabota(url.address)
    # print(city, specialty, site, url.address)
    
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=city, specialty=specialty, site=site,
                                title=job['title'] , url=job['href'], 
                                description=job['descript'], 
                                company=job['company'])
            vacancy.save()
        
    
    return render(request, 'scraping/home.html', {'jobs': jobs})
    
def dou_scraping(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    site = Site.objects.get(name='Dou.ua')
    url = Url.objects.get(city=city, specialty=specialty, site=site)
    vacancy = Vacancy.objects.filter(city=city, specialty=specialty, site=site, 
                                    timestamp__gte=TWO_DAYS_AGO).values('url')
    vacancy_url_list = [i['url'] for i in vacancy]
    jobs = []
    jobs = dou(url.address)
    # print(city, specialty, site, url.address)
    
    for job in jobs:
        if job['href'] not in vacancy_url_list:
            vacancy = Vacancy(city=city, specialty=specialty, site=site,
                                title=job['title'] , url=job['href'], 
                                description=job['descript'], 
                                company=job['company'])
            vacancy.save()
        
    
    return render(request, 'scraping/home.html', {'jobs': jobs})