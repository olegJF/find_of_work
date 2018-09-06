import os, sys

project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'vacancy.settings'
import django
django.setup()


from scraping.utils import *


def save_to_db():
    url = 'https://www.work.ua/jobs-kyiv-python/?days=122'
    j, e = [], []
    j, e = work(url, stop_list = [])
    print('Jobs', len(j))
    print('Errors', len(e))
        
    return True
    
if __name__ == '__main__':
    save_to_db()
    print('Done!')