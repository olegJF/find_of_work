from django.db import models
from scraping.models import City, Specialty


class Subscriber(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    city = models.ForeignKey(City, verbose_name='Город')
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность')
    email = models.CharField(max_length=50, verbose_name='Имэйл', unique=True)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['name']

    def __str__(self):
        return self.name
