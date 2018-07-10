import os
import psycopg2
import logging
import datetime
import requests

dir = os.path.dirname(os.path.abspath('send_emails.py'))
path = ''.join([dir, '\\vacancy\\settings\\secret.py'])

if os.path.exists(path):
    print('File exists')
    from vacancy.settings.secret import (EMAIL, MAILGUN_KEY, DB_PASSWORD, 
                                            DB_HOST, DB_NAME, DB_USER)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    EMAIL = os.environ.get('EMAIL')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')

ADDRESS = "https://api.mailgun.net/v3/sandbox62c562b960c34f34bec9fd5a60c087b2.mailgun.org/messages"
today = datetime.date.today()

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
    sub_qs = set(cur.fetchall())
    # print(cities_qs)
    cities_id = set([i[0] for i in sub_qs])
    specialties_id = set([i[1] for i in sub_qs])
    cities = {}
    for i in cities_id:
        cur.execute("""SELECT name FROM scraping_city WHERE id=%s;""", (i,))
        qs = cur.fetchone()
        cities[i] = qs[0]
    specialties = {}
    for i in specialties_id:
        cur.execute("""SELECT name FROM scraping_specialty WHERE id=%s;""", (i,))
        qs = cur.fetchone()
        specialties[i] = qs[0]
    missing_urls = []
    for pair in sub_qs:
        cur.execute("""SELECT id FROM scraping_url 
                    WHERE city_id=%s AND specialty_id=%s;""",(pair[0], pair[1] ))
        qs = cur.fetchall()
        if not qs:
            missing_urls.append((cities[pair[0]], specialties[pair[1]]))
    if missing_urls:
        cntnt = 'На дату {}, отсутствуют урлы для следующих пар:\n'.format(today)
        for pair in missing_urls:
            cntnt += 'город - {}, специальность - {}\n'.format(pair[0], pair[1])
        
        Subject = 'Отсутствующие урлы в БД, по состояниию на {}'.format(today)
        requests.post( ADDRESS, auth=("api", MAILGUN_KEY), 
                            data={"from": EMAIL, "to": 'jf2@ua.fm',
                            "subject": Subject, "text": cntnt})
    cur.execute("""SELECT data FROM scraping_error WHERE timestamp=%s;""",
                (today,))
    errors_qs = cur.fetchone()
    if errors_qs:
        # print('qs')
        data = errors_qs[0]['errors']
        cntnt = 'На дату {}, следующие ошибки:\n'.format(today)
        for err in data:
            cntnt += 'url - {}, причина - {}\n'.format(err['href'], err['title'])
        
        Subject = 'Ошибки скрапинга, по состояниию на {}'.format(today)
        requests.post( ADDRESS, auth=("api", MAILGUN_KEY), 
                            data={"from": EMAIL, "to": 'find_it_1@ukr.net',
                            "subject": Subject, "text": cntnt})

    # print('Done!')
    
    conn.commit()
    cur.close()
    conn.close()

