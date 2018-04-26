# from vacancy.settings.secret import DB_PASSWORD
from scraping.utils import *
import os
import psycopg2
import logging
import datetime

dir = os.path.dirname(os.path.abspath('send_emails.py'))
path = ''.join([dir, '\\vacancy\\settings\\secret.py'])

if os.path.exists(path):
    print('File exists')
    from vacancy.settings.secret import (DB_PASSWORD, DB_HOST, DB_NAME, DB_USER)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
# print(DB_PASSWORD, DB_HOST,  DB_NAME, DB_USER, )


today = datetime.date.today()
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                            password=DB_PASSWORD)
    # print('Opened DB')
except:
    logging.exception('Unable to open DB - {}'.format(today))

else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, specialty_id FROM subscribers_subscriber 
                    WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    # print(cities_qs)
    todo_list = {i[0]: set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    print(todo_list)
    cur.execute("SELECT * FROM scraping_site;")
    sites_qs = cur.fetchall()
    sites = {i[0]: i[1] for i in sites_qs}
    url_list = []
    tmp_city = {}
    for city in todo_list:
        for sp in todo_list[city]:
            tmp = {}
            cur.execute("""SELECT site_id, address FROM scraping_url 
                        WHERE city_id=%s AND specialty_id=%s;""",(city, sp ))
            qs = cur.fetchall()
            # print(qs)
            if qs:
                tmp['city'] = city
                tmp['specialty'] = sp
                for item in qs:
                    site_id = item[0]
                    tmp[sites[site_id]] = item[1]
                url_list.append(tmp)
    # print(url_list)
    all_data = []
    for url in url_list:
        tmp = {}
        tmp_content = []
        tmp_content.extend(djinni(url['Djinni.co']))
        tmp_content.extend(work(url['Work.ua']))
        tmp_content.extend(rabota(url['Rabota.ua']))
        tmp_content.extend(dou(url['Dou.ua']))
        tmp['city'] = url['city']
        tmp['specialty'] = url['specialty']
        tmp['content'] = tmp_content
        all_data.append(tmp)
    # print('scraping_list')

   #   cur.execute("SET TIME ZONE 'Europe/Kiev';")
    if all_data:
        for data in all_data:
            city = data['city']
            specialty = data['specialty']
            jobs = data['content']
            jobs.reverse()
            for job in jobs:
                cur.execute("""SELECT * FROM scraping_vacancy WHERE url=%s;""", 
                                (job['href'],))
                qs = cur.fetchone()
                if not qs:
                    cur.execute("""INSERT INTO scraping_vacancy (city_id,
                        specialty_id, title, url, description, company, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (city, specialty, job['title'], job['href'],
                        job['descript'], job['company'], today))



 #    # print('Done')
    conn.commit()
    cur.close()
    conn.close()
