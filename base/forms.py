from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import  Room,Ploeg,Locker,Person
from django import forms
import io
import csv
from django.core.exceptions import ValidationError

FORMAT_CHOICES=(
    ('xls','xls'),
    ('csv','csv'),
    ('json','json'),
)

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        # model = User
        # fields = '__all__'
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
        "username": "Your email address cq. username",
        }

class WachtlijstForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['hoofdhuurder', 'onderhuur']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class FormatForm(forms.Form):
    format=forms.ChoiceField(choices=FORMAT_CHOICES,widget=forms.Select(attrs={'class':'form-select'}))

class LockerForm(ModelForm):
    class Meta:
        model = Locker
        # fields = '__all__'
        fields = ['email','locker','nieuwe_huurder','vorige_huurder','label','type','topic','verhuurd','opgezegd','obsolete','tekst','sleutels','code','opzegdatum',]
        exclude = ['opzegdatum','kluisje','obsolete','opgezegd','topic','kluisnummer']
        labels = {
        "verhuurd": "Verhuurd",
        "topic": "nieuwe benaming",
        "kluisje": "vorige benaming",
        "tekst": "Mede gebruikers",
        "sleutels": "Aantal Sleutels in omloop",
        "code": "Code van codeslot",
        # "type": "Type slot",

        }
class LockerFormAdmin(ModelForm):
    class Meta:
        model = Locker
        fields = '__all__'
        # fields = ['email','kluisnummer','nieuwe_huurder','vorige_huurder','kluisje','type','topic','verhuurd','opgezegd','obsolete','tekst','sleutels','code','opzegdatum',]
        # exclude = ['type','code','opzegdatum','kluisje','obsolete','opgezegd','topic','verhuurd','kluisnummer']
        labels = {
        "verhuurd": "Bent u hoofdhuurder?",
        "topic": "nieuwe benaming",
        "kluisje": "vorige benaming",
        "tekst": "Mede gebruikers",
        "sleutels": "Aantal Sleutels in omloop",
        "code": "Code van codeslot",
        "type": "Type slot",

        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields= '__all__'
        # fields = ['avatar', 'username','locker', 'email']
        exclude = [ 'avatar','ploeg','bio','user_permissions','date_joined','groups','password','is_staff','is_superuser','is_active','last_name','last_login']
        labels = {
        "first_name": "Short Name",
        "username": "unieke naam",
        # "locker" : "Huurder van:"
        }

