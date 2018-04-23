import requests
from bs4 import BeautifulSoup as BS
import codecs
import time
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def djinni(base_url, stop_list = ['Senior', 'Sr.']):
    base_url = base_url
    session = requests.Session()
    urls, jobs = [], []
    urls.append(base_url)
    urls.append(base_url+'&page=2')
    a_href = 'https://djinni.co'
    for url in urls:
        req = session.get(url, headers=headers)
        time.sleep(2)
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            list_of_li = bsObj.find_all('li', attrs={'class':'list-jobs__item'})
            if list_of_li:
                for li in list_of_li:
                    div = li.find('div', attrs={'class':'list-jobs__title'})
                    # print('div', div.a['href'], div.a.text)
                    div_description = li.find('div', attrs={'class':'list-jobs__description'})
                    descr='No Discription!'
                    title = div.a.text
                    if div_description:
                        descr=div_description.p.text
                    title_list = title.split(' ')
                    if not any(word in stop_list for word in title_list):
                        jobs.append({'href': a_href+div.a['href'], 
                                        'title': title, 
                                        'descript': str(descr),
                                        'company': 'No name'})
                                        
            else:
                jobs.append({'href': url, 
                                'title': 'The page is empty',
                                'descript': '', 'company': ''
                                    })
        else:
            jobs.append({'href': base_url, 
                            'title': 'Page do not response',
                            'descript': '', 'company': ''
                                })
    return jobs
    
def work(base_url, stop_list = ['Senior', 'Sr.']):
    session = requests.Session()
    urls, jobs = [], []
    urls.append(base_url)
    a_href = 'https://www.work.ua'
    req = session.get(base_url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        pagination = bsObj.find('ul', attrs={'class':'pagination'})
        if pagination:
            pages = pagination.find_all('li', attrs={'class':False})
            for page in pages:
                urls.append(a_href+page.a['href'])
        
    else:
        jobs.append({'href': base_url, 
                        'title': 'Page do not response',
                        'descript': '', 'company': ''
                            })    
    for url in urls:
        time.sleep(2)
        req = session.get(url, headers=headers)
        if req.status_code == 200:
            list_of_div = bsObj.find_all('div', attrs={'class':'job-link'})
            if list_of_div:
                for div in list_of_div:
                    company = 'No name'
                    h2 = div.find('h2')
                    logo = div.find('div', attrs={'class':'logo-img'})
                    if logo:
                        company = logo.img['alt']
                    title = h2.a.text
                    title_list = title.split(' ')
                    if not any(word in stop_list for word in title_list):
                        jobs.append({'href': a_href+div.a['href'], 
                                        'title': h2.a['title'],
                                        'descript': str(div.p.text), 
                                        'company': company
                                        })
            else:
                jobs.append({'href': url, 
                                'title': 'The page is empty',
                                'descript': '', 'company': ''
                                    })
        else:
            jobs.append({'href': url, 
                            'title': 'Page do not response',
                            'descript': '', 'company': ''
                                })
    return jobs

    
def rabota(base_url, stop_list = ['Senior', 'Sr.']):
    yesterday=datetime.date.today()-datetime.timedelta(1)
    from_day = yesterday.strftime('%d.%m.%Y')
    base_url = base_url + from_day
    session = requests.Session()
    urls, jobs = [], []
    urls.append(base_url)
    a_href = 'https://rabota.ua'
    
    req = session.get(base_url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
        dl = bsObj.find('dl', attrs={'id':'content_vacancyList_gridList_pagerInnerTable'})
        if dl:
            pages = dl.find_all('a', attrs={'class':'f-always-blue'})
            if pages:
                for p in pages:
                    urls.append(a_href+p['href'])
    else:
        jobs.append({'href': base_url, 
                        'title': 'Page do not response',
                        'descript': '', 'company': ''
                            })
    for url in urls:
        time.sleep(2)
        req = session.get(url, headers=headers)
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            table = bsObj.find('table', attrs={'id':'content_vacancyList_gridList'})
            if table:
                list_of_tr = table.find_all('tr', attrs={'id':True})
                for tr in list_of_tr:
                    company = 'No name of company'
                    h3 = tr.find('h3')
                    title = h3.a.text
                    logo = tr.find('p', attrs={'class':'f-vacancylist-companyname'})
                    if logo:
                        company = logo.text
                    # posted = ''
                    # when_posted = tr.find('p', attrs={'class':'f-vacancylist-agotime'})
                    # if when_posted:
                    #     posted = when_posted.text
                    descr = tr.find('p', attrs={'class':'f-vacancylist-shortdescr'}).text
                    title_list = title.split(' ')
                    if not any(word in stop_list for word in title_list):
                        jobs.append({'href': a_href+h3.a['href'], 
                                        'title': title, # +' , '+posted,
                                        'descript':str(descr), 
                                        'company': company
                                            })
            else:
                jobs.append({'href': url, 
                                'title': 'The page is empty',
                                'descript': '', 'company': ''
                                    })
        else:
            jobs.append({'href': url, 
                            'title': 'Page do not response',
                            'descript': '', 'company': ''
                                })
    return jobs

def dou(base_url, stop_list = ['Senior', 'Sr.']):
    session = requests.Session()
    urls, jobs = [], []
    urls.append(base_url)
    a_href = 'https://www.dou.ua'
    req = session.get(base_url, headers=headers)
    if req.status_code == 200:
        bsObj = BS(req.content, "html.parser")
       
        div = bsObj.find('div', attrs={'id':'vacancyListId'})
        if div:
            vacancy_list = div.find_all('li', attrs={'class':'l-vacancy'})
            for v in vacancy_list:
                company = 'No name'
                link = v.find('a', attrs={'class':'vt'})
                title = link.text
                firm = v.find('a', attrs={'class':'company'})
                company = firm.text
                desc = v.find('div', attrs={'class':'sh-info'})
                title_list = title.split(' ')
                if not any(word in stop_list for word in title_list):
                    jobs.append({'href': link['href'], 
                                    'title': title,
                                    'descript':str(desc.text), 
                                    'company': company
                                        })
        else:
            jobs.append({'href': url, 
                            'title': 'The page is empty',
                            'descript': '', 'company': ''
                                })
    else:
        jobs.append({'href': url, 
                        'title': 'Page do not response',
                        'descript': '', 'company': ''
                            })                                
                                    
    return jobs
                                        