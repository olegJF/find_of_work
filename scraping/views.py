from django.shortcuts import render
from django.http import HttpResponse
import datetime

from .models import *
from .forms import FindVacancyForm


def home(request):
    form = FindVacancyForm
    return render(request, 'scraping/home.html', {'form': form})


def vacancy_list(request):
    if request.GET:
        city = int(request.GET.get('city'))
        specialty = int(request.GET.get('specialty'))
        qs = ''
        if city and specialty:
            qs = Vacancy.objects.filter(city=city, specialty=specialty)
            city = City.objects.get(id=city)
            specialty = Specialty.objects.get(id=specialty)
        
        form = FindVacancyForm
        return render(request, 'scraping/list.html', {'form': form, 
                                    'object_list': qs, 'city_name': city.name, 'specialty_name': specialty.name})
    else:
        form = FindVacancyForm
    return render(request, 'scraping/list.html', {'form': form,})

        
