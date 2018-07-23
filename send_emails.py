import os
import smtplib
import psycopg2
import logging
import datetime
import requests
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dir = os.path.dirname(os.path.abspath('send_emails.py'))
path = ''.join([dir, '\\vacancy\\settings\\secret.py'])

if os.path.exists(path):
    # print('File exists')
    from vacancy.settings.secret import (DB_PASSWORD, DB_HOST, MAILGUN_KEY,
                                        DB_NAME, DB_USER, PASSWORD, EMAIL,
                                        API_ADDRESS, MAIL, PASSWORD_AWARD, 
                                        USER_AWARD, FROM_EMAIL, TO_EMAIL )
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    PASSWORD = os.environ.get('PASSWORD')
    EMAIL = os.environ.get('EMAIL')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')
    API_ADDRESS = os.environ.get('API_ADDRESS')

# FROM_EMAIL = 'Вакансии <{email}>'.format(email=EMAIL)
# SUBJECT = 'Список вакансий'
ONE_DAY_AGO = datetime.date.today()-datetime.timedelta(1)
today = datetime.date.today()
#Subject = 'Список вакансий за  {}'.format(today)
template = """<!doctype html><html lang="en"><head><meta charset="utf-8">
                </head><body> <h2> Список вакансий по состоянию на {} </h2>
                <hr/><br/> """.format(today)
end = '</body></html>'

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Список вакансий за  {}'.format(today)
msg['From'] = 'Вакансии <{email}>'.format(email=FROM_EMAIL)


try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                            password=DB_PASSWORD)
    # print('Opened DB')
except psycopg2.DatabaseError:
    logging.exception('Unable to open DB - {}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, specialty_id FROM subscribers_subscriber
                    WHERE is_active=%s;""", (True,))
    data_of_requests = set(cur.fetchall())
    # print(data_of_requests)
    mail = smtplib.SMTP(MAIL, 587)
    mail.ehlo()
    mail.starttls()
    mail.login(USER_AWARD, PASSWORD_AWARD)
    for pair in data_of_requests:
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
        if jobs_qs:
            for job in jobs_qs:
                content += '<a href="{}" target="_blank">'.format(job[0])
                content += '{}</a>'.format(job[1])
                content += '<br/><p>{}</p><br/>'.format(job[2])
                content += '<hr><br/>'
            html_message = template + content + end
            part = MIMEText(html_message, 'html')
            msg.attach(part)
            for email in emails:
                msg['To'] = email
                mail.sendmail(FROM_EMAIL, email, msg.as_string())
                time.sleep(2)

                # requests.post( API_ADDRESS, auth=("api", MAILGUN_KEY),
                #                 data={"from": FROM_EMAIL, "to": email,
                #                 "subject": Subject, "html": html_message})
        else:
            text = 'На сегодня, список вакансий по Вашему запросу, пуст.'
            part = MIMEText(text, 'plain')
            msg.attach(part)
            for email in emails:
                msg['To'] = email
                mail.sendmail(FROM_EMAIL, email, msg.as_string())
                time.sleep(2)
    # print('Done')
    conn.commit()
    cur.close()
    conn.close()
    mail.quit()
