from django import forms
from .models import *
from scraping.models import Specialty, City

class SubscriberModelForm(forms.ModelForm):
    name = forms.CharField(label='Ваше имя', required=True,
                           widget=forms.TextInput(attrs={"class": 'form-control'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))
    specialty = forms.ModelChoiceField(label='Специальность', queryset=Specialty.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))
    email = forms.EmailField(label='Email', required=True,
                           widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
                                            attrs={"class": 'form-control'}))
    is_active = forms.BooleanField(label='Получать рассылку?',
                                required=False, widget=forms.CheckboxInput())
    
    class Meta(object):
        model = Subscriber
        fields = ('name', 'city', 'specialty', 'email', 'password', 'is_active')
        

class LogInForm(forms.Form):
    
    email = forms.EmailField(label='Email', required=True,
                           widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
                                            attrs={"class": 'form-control'}))
                                            
    def clean_password(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print('fgh')
        if password and email:
            qs = Subscriber.objects.filter(email=email, password=password).first()
            print(qs)
            if qs == None:
                raise forms.ValidationError('Пользователя с таким имейлом и паролем не существует')
        return email
        
    
    
class SubscriberHiddenEmailForm(forms.ModelForm):
    name = forms.CharField(label='Ваше имя', required=True,
                           widget=forms.TextInput(attrs={"class": 'form-control'}))
    city = forms.ModelChoiceField(label='Город', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))
    specialty = forms.ModelChoiceField(label='Специальность', queryset=Specialty.objects.all(),
                                     widget=forms.Select(attrs={"class": 'form-control js-example-basic-single'}))
    email = forms.EmailField(widget=forms.HiddenInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
                                            attrs={"class": 'form-control'}))
    is_active = forms.BooleanField(label='Получать рассылку?',
                                required=False, widget=forms.CheckboxInput())
    
    class Meta(object):
        model = Subscriber
        fields = ('name', 'city', 'specialty', 'email', 'password', 'is_active')