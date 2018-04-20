from vacancy.settings.secret import PASSWORD, EMAIL, DB_PASSWORD


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



import psycopg2
import logging
import datetime

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = PASSWORD
EMAIL_PORT = 587
EMAIL_USE_TLS = True
FROM_EMAIL = 'Vacancy <{email}>'.format(email=EMAIL)
SUBJECT = 'Vacancy list'



ONE_DAY_AGO = datetime.date.today()-datetime.timedelta(1)


today = datetime.date.today()
try:
    conn = psycopg2.connect(dbname='vacancy', user='postgres', host='localhost', password=DB_PASSWORD)
    # print('Opened DB')
except:
    logging.exception('Unable to open DB - {}'.format(today))
    
else:
    cur = conn.cursor()
    cur.execute("SELECT city_id, specialty_id FROM subscribers_subscriber WHERE is_active=%s;", (True,))
    data_of_requests = set(cur.fetchall())
    # print(data_of_requests)

    for pair in data_of_requests:
        template = '<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
        end = '</body></html>'
        content = ''
        city = pair[0]
        specialty = pair[1]
        cur.execute("""SELECT email FROM subscribers_subscriber 
                    WHERE city_id=%s AND specialty_id=%s AND is_active=%s;""", 
                    (city, specialty,True,))
                    
        email_qs = cur.fetchall()
        
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url, title, description FROM scraping_vacancy WHERE city_id=%s 
        AND specialty_id=%s AND timestamp=%s;""", 
                    (city, specialty,datetime.date.today(),))
        jobs_qs = cur.fetchall()
        # print(str(jobs_qs).encode('utf-8'))         
        
        # jobs_qs = Vacancy.objects.filter(city=city, specialty=specialty,
        #                             timestamp=datetime.date.today())
        for job in jobs_qs:
            content += '<a href="{}" target="_blank">'.format(job[0])
            content += '{}</a>'.format(job[1])
            content += '<br/><p>{}</p><br/>'.format(job[2])
            content += '<hr><br/>'
        template = template + content + end
        for email in emails:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = SUBJECT
            msg['From'] = FROM_EMAIL
            msg['To'] = email
            # recipient_list = [email]
            text = 'This is an important message.'
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(template, 'html')

            msg.attach(part1)
            msg.attach(part2)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.connect('smtp.gmail.com', 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(EMAIL, PASSWORD)
            s.sendmail(FROM_EMAIL, email, msg.as_string())
            s.quit()
        # print(str(template).encode('utf-8'))
    # return HttpResponse( '<h1>God!</h1>')
   
    print('Done')
    conn.commit()
    cur.close()
    conn.close()