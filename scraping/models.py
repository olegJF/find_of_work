from django.db import models

class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Город')
    
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
    
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'
        ordering = ['name']

    def __str__(self):
        return self.name
 
        
class Url(models.Model):
    city = models.ForeignKey(City, verbose_name='Город')
    site = models.ForeignKey(Site, verbose_name='Название сайта для поиска')
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность')
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
    city = models.ForeignKey(City, verbose_name='Город')
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность')
    timestamp = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


