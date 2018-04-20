from django.contrib import admin
from .models import *


class VacancyAdmin(admin.ModelAdmin):

    class Meta:
        model = Vacancy
    list_display = ('title', 'url', 'specialty', 'city', 'timestamp')


admin.site.register(City)
admin.site.register(Site)
admin.site.register(Specialty)
admin.site.register(Url)
admin.site.register(Vacancy, VacancyAdmin)
