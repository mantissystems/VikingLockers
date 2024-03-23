from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import  Room,Ploeg,Locker,Person
import io
from django import forms
import csv
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

FORMAT_CHOICES=(
    ('xls','xls'),
    ('csv','csv'),
    ('json','json'),
)
# class DataForm(forms.Form):
#     data_file= forms.FileField()
#     model=User
#     def process_data(self):
#         f=io.TextIOWrapper(self.changed_data['data_file'])
#         reader=csv.DictReader(f)
#         for user in reader:
#             User.objects.update_or_create(
#                 username=user['username'],
#                 email=user['email']
#             )

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ['username', 'email', 'password1', 'password2']

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         # fields = ['first_name', 'username', 'email', 'password1', 'password2']
#         fields = ['first_name',  'email', 'password1', 'password2']
#         labels = {
#         "email": "Your email. eg.: info@mail.nl",
#         "password1": "wil in flexpoule",
#         "Password2": "deel mij in als host",
#         # "username": "Your app-username",
#         "name": "Your name",
#         }

# class PersonForm(ModelForm):
#     def __init__(self,*args,**kwargs):
#         self.email = kwargs.pop('personmail')
#         super(PersonForm,self).__init__(*args,**kwargs)
#     class Meta:
#         model = Person
#         fields = '__all__'
# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'

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
        fields = ['email','kluisnummer','nieuwe_huurder','vorige_huurder','kluisje','type','topic','verhuurd','opgezegd','obsolete','tekst','sleutels','code','opzegdatum',]
        exclude = ['type','code','opzegdatum','kluisje','obsolete','opgezegd','topic','verhuurd','kluisnummer']
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

