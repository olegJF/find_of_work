from django.shortcuts import render
from django.http import HttpResponse, Http404
import datetime

from .models import *
from .forms import FindVacancyForm


def home(request):
    form = FindVacancyForm
    return render(request, 'scraping/home.html', {'form': form})


def vacancy_list(request):
    form = FindVacancyForm
    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            specialty_id = int(request.GET.get('specialty'))
        except ValueError:
            raise Http404("Страница не найдена")
        context = {}
        qs = Vacancy.objects.filter(city=city_id, specialty=specialty_id)
        if qs:
            context = {'form': form, 'object_list': qs, 
                        'city_name': qs[0].city.name, 
                        'specialty_name': qs[0].specialty.name}
                                
        return render(request, 'scraping/list.html', context)

    return render(request, 'scraping/list.html', {'form': form,})

        
