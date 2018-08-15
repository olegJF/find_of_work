from django.db import models
from django.contrib.postgres.fields import JSONField

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Город')
    slug = models.SlugField(blank=True)
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

    def __str__(self):
        return self.name
        

class Site(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название сайта для поиска')
    
    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайты'
        ordering = ['name']

    def __str__(self):
        return self.name
        

class Specialty(models.Model):
    name = models.CharField(max_length=50, verbose_name='Специальность')
    slug = models.SlugField(blank=True)
    
    
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['name']

    def __str__(self):
        return self.name
 
        
class Url(models.Model):
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    site = models.ForeignKey(Site, verbose_name='Название сайта для поиска', on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность', on_delete=models.CASCADE)
    address = models.URLField(max_length=250, verbose_name='url')
    
    class Meta:
        verbose_name = 'Адрес для поиска'
        verbose_name_plural = 'Адреса для поиска'
        ordering = ['specialty', 'city']

    def __str__(self):
        return 'Специальность {} в г. {} на сайте {}'.format(self.specialty, self.city, self.site)
                

class Vacancy(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    url = models.CharField(max_length=250, verbose_name='Интернет адрес вакансии', unique=True, default=None)
    description = models.TextField(verbose_name='Описание вакансии', blank=True)
    company = models.CharField(max_length=250, verbose_name='Вакансия от компании', blank=True)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность', on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    data = JSONField()
    timestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ошибки скрапинга'
        verbose_name_plural = 'Ошибки скрапинга'
        ordering = ['-timestamp']

    def __str__(self):
        return self.timestamp.strftime('%Y-%m-%d')