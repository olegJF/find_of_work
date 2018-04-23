import os
import psycopg2
import logging
import datetime

WEEK_AGO = datetime.date.today()-datetime.timedelta(7)
dir = os.path.dirname(os.path.abspath('send_emails.py'))
path = ''.join([dir, '\\vacancy\\settings\\secret.py'])

if os.path.exists(path):
    # print('File exists')
    from vacancy.settings.secret import (DB_PASSWORD, DB_HOST, DB_NAME, DB_USER)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')

# print(WEEK_AGO)
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST,
                            password=DB_PASSWORD)
    # print('Opened DB')
except:
    logging.exception('Unable to open DB - {}'.format(today))

else:
    cur = conn.cursor()
    cur.execute("""DELETE FROM scraping_vacancy WHERE timestamp <=%s;""", 
                            (WEEK_AGO,))
    # qs = cur.fetchall()
    # print(len(qs))
    conn.commit()
    cur.close()
    conn.close()

