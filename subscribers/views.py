import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import DetailView, FormView, UpdateView, DeleteView
from .models import Subscriber
from .forms import (SubscriberModelForm, 
                    LogInForm,
                    SubscriberHiddenEmailForm,
                    ContactForm)

try:
    from vacancy.settings.secret import (EMAIL, MAILGUN_KEY )
except:
    EMAIL = os.environ.get('EMAIL')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')

ADDRESS = "https://api.mailgun.net/v3/sandbox62c562b960c34f34bec9fd5a60c087b2.mailgun.org/messages"

class SubscriberCreate(FormView):
    form_class = SubscriberModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('home')
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, 'Данные успешно сохранены!')
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    
def login_subscriber(request):
    if request.method == "GET":
        form = LogInForm
        return render(request, 'subscribers/login.html', {"form": form})
    elif request.method == "POST":
        form = LogInForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')
        return render(request, 'subscribers/login.html', {"form": form})

        
def update_subscriber(request):
    if request.method == "GET" and request.session.get('email', False):
        email = request.session.get('email')
        qs = Subscriber.objects.filter(email=email).first()
        
        form = SubscriberHiddenEmailForm(initial={'name': qs.name, 'city': qs.city, 
                        'specialty': qs.specialty, 'email': qs.email, 
                        'password': qs.password, 'is_active': qs.is_active})
        return render(request, 'subscribers/update.html', {'form': form})
    elif request.method == "POST":
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = SubscriberHiddenEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно сохранены')
            return redirect('home')
        messages.error(request, 'Необходимо корректно заполнить  все поля формы')
        return render(request, 'subscribers/update.html', {'form': form})
            
    else:
        form = LogInForm
        return render(request, 'subscribers/login.html', {"form": form})


def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            specialty = form.cleaned_data['specialty']
            from_email = form.cleaned_data['from_email']
            content = 'Прошу добавить в поиск, город - {}'.format(city)
            content += ', специальность - {}.'.format(specialty)
            content += 'Запрос отправлен от  {}'.format(from_email)
            Subject = 'Запрос на добавление в БД'
            requests.post( ADDRESS, auth=("api", MAILGUN_KEY), 
                                data={"from": EMAIL, "to": 'jf2@ua.fm',
                                "subject": Subject, "text": content})
            messages.success(request, 'Письмо успешно отправленно!')

            return redirect('home')
        return render(request, 'subscribers/form.html', {'form': form})
    
    else:
        form = ContactForm()

    return render(request, 'subscribers/form.html', {'form': form})