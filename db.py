from vacancy.settings.secret import PASSWORD
from scraping.utils import *

import psycopg2
import logging

try:
    conn = psycopg2.connect(dbname='vacancy', user='postgres', host='localhost', password=PASSWORD)
    print('Opened DB')
except:
    logging.exception('Unable to open DB')
    
else:
    cur = conn.cursor()
    cur.execute("SELECT city_id FROM subscribers_subscriber WHERE is_active=TRUE;")
    cities_qs = cur.fetchall()
    cities = set([i[0] for i in cities_qs])
    todo_list = {}
    for city in cities:
        cur.execute("SELECT specialty_id FROM subscribers_subscriber WHERE city_id=%s;", (city,))
        sp_qs = cur.fetchall()
        tmp = set([i[0] for i in sp_qs])
        todo_list[city] = tmp
    
    cur.execute("SELECT * FROM scraping_site;")
    sites_qs = cur.fetchall()
    sites = {i[0]: i[1] for i in sites_qs}
    url_list = []
    tmp_city = {}
    for city in todo_list:
        for sp in todo_list[city]:
            tmp = {}
            cur.execute("SELECT site_id, address FROM scraping_url WHERE city_id=%s AND specialty_id=%s;",(city, sp ))
            qs = cur.fetchall()
            # print(qs)
            tmp['city'] = city
            tmp['specialty'] = sp
            for item in qs:
                site_id = item[0]
                tmp[sites[site_id]] = item[1]
            url_list.append(tmp)
        
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
        
            
    # print(str(jobs).encode('utf-8'))
    cur.close()
    conn.close()