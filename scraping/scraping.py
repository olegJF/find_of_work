from django.db import IntegrityError

from .models import *
from subscribers.models import *
from .utils import *


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


def save_to_db():
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
        
    return True

if __name__ == '__main__':
    save_to_db()
    print('Done!')