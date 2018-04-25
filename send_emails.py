import os
import smtplib
import psycopg2
import logging
import datetime

import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dir = os.path.dirname(os.path.abspath('send_emails.py'))
path = ''.join([dir, '\\vacancy\\settings\\secret.py'])

if os.path.exists(path):
    # print('File exists')
    from vacancy.settings.secret import (DB_PASSWORD, DB_HOST, EMAIL,
                                        DB_NAME, DB_USER, PASSWORD, MAILGUN_KEY
                                        )
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    PASSWORD = os.environ.get('PASSWORD')
    EMAIL = os.environ.get('EMAIL')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')

ADDRESS = "https://api.mailgun.net/v3/sandbox62c562b960c34f34bec9fd5a60c087b2.mailgun.org/messages"

FROM_EMAIL = 'Vacancy <{email}>'.format(email=EMAIL)
SUBJECT = 'Список вакансий'
ONE_DAY_AGO = datetime.date.today()-datetime.timedelta(1)
today = datetime.date.today()

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                            password=PASSWORD)
    # print('Opened DB')
except psycopg2.DatabaseError:
    logging.exception('Unable to open DB - {}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, specialty_id FROM subscribers_subscriber
                    WHERE is_active=%s;""", (True,))
    data_of_requests = set(cur.fetchall())
    # print(data_of_requests)

    for pair in data_of_requests:
        template = """<!doctype html><html lang="en"><head>
                        <meta charset="utf-8"></head><body>
                        <h2> Список вакансий по состоянию на {} </h2>
                        <hr><br/> """.format(today)
        end = '</body></html>'
        content = ''
        city = pair[0]
        specialty = pair[1]
        cur.execute("""SELECT email FROM subscribers_subscriber
                    WHERE city_id=%s AND specialty_id=%s AND is_active=%s;""",
                    (city, specialty, True,))

        email_qs = cur.fetchall()

        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url, title, description FROM scraping_vacancy 
                    WHERE city_id=%s AND specialty_id=%s AND timestamp=%s;""",
                    (city, specialty, datetime.date.today(),))
        jobs_qs = cur.fetchall()
        # print(str(jobs_qs).encode('utf-8'))

        # jobs_qs = Vacancy.objects.filter(city=city, specialty=specialty,
        #                             timestamp=datetime.date.today())
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a>'.format(job[1])
                content += '<br/><p>{}</p><br/>'.format(job[2])
                content += '<hr><br/>'
            template = template + content + end
            for email in emails:
                Subject = 'Список вакансий за  {}'.format(today)
                requests.post( ADDRESS, auth=("api", MAILGUN_KEY), 
                                data={"from": EMAIL, "to": email,
                                "subject": Subject, "html": template})

        # print(str(template).encode('utf-8'))
    # return HttpResponse( '<h1>God!</h1>')

    # print('Done')
    conn.commit()
    cur.close()
    conn.close()
