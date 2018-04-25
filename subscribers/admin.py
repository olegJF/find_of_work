from django.contrib import admin
from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):

    class Meta:
        model = Subscriber
    list_display = ('name', 'email', 'specialty', 'city', 'is_active')
    list_editable = ['is_active']

admin.site.register(Subscriber, SubscriberAdmin)
