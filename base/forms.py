from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User,Ploeg,Locker,Excellijst
import io
from django import forms
import csv

class DataForm(forms.Form):
    data_file= forms.FileField()
    model=User
    def process_data(self):
        f=io.TextIOWrapper(self.changed_data['data_file'])
        reader=csv.DictReader(f)
        for user in reader:
            User.objects.update_or_create(
                username=user['username'],
                email=user['email']
            )

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
        exclude = ['username']
        labels = {
        "email": "Your email. eg.: info@mail.nl",
        "password": "minimum length 8",
        "password2": "deel mij in als host",
        "username": "Your app-username",
        "name": "Your name",
        }

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class PloegForm(ModelForm):
    class Meta:
        model = Ploeg
        fields = '__all__'
        exclude=['participants']
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     widgets = {
        #     'category': forms.CheckboxSelectMultiple
        # }
        #     widgets = {
        #     'persons': forms.SelectMultiple(attrs={'readonly': 'True', 'disabled': 'True'})
        # }
        #     where1='is_active=True'
        #     self.fields['participants'].widget.attrs.update(size='20')
        #     self.fields['participants'].queryset=User.objects.filter(where1).order_by('name')[0:2]
class LockerForm(ModelForm):
    class Meta:
        model = Locker
        fields = '__all__'
        labels = {
        "verhuurd": "Verhuurd",
        "owners": "onder huurders",
        "sleutels": "Aantal Sleutels in omloop",
        "code": "Code van codeslot",
        "kluisje": "Locker nummer",
        "type": "Type slot",

        }
        exclude = ['topic','row', 'col','owners','kluisnummer','verhuurd']
        # exclude = ['topic','row', 'col','owners']
class ExcelForm(ModelForm):
    class Meta:
        model = Excellijst
        fields = '__all__'
        # labels = {
        # "verhuurd": "Verhuurd",
        # "owners": "onder huurders",
        # "sleutels": "Aantal Sleutels in omloop",
        # "code": "Code van codeslot",
        # "kluisje": "Locker nummer",
        # "type": "Type slot",

        # }
        # exclude = ['topic','row', 'col','owners','kluisnummer','verhuurd']


class UserForm(ModelForm):
    class Meta:
        model = User
        # fields= '__all__'
        fields = ['avatar', 'name', 'username','locker', 'email']
        exclude = [ 'avatar','ploeg','bio']
