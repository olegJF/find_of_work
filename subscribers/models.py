from django.db import models
from scraping.models import City, Specialty


class SubscriberQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(is_active=True)
        
        
class SubscriberManager(models.Manager):
    
    def get_queryset(self):
        return SubscriberQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


class Subscriber(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    city = models.ForeignKey(City, verbose_name='Город')
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность')
    email = models.CharField(max_length=50, verbose_name='Имэйл', unique=True)
    is_active = models.BooleanField(default=True)
    
    objects = SubscriberManager()

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ['name']

    def __str__(self):
        return self.name
