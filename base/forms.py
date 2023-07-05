from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User,Ploeg,Locker
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
        labels = {
        "email": "Your email. eg.: info@mail.nl",
        "password1": "wil in flexpoule",
        "Password2": "deel mij in als host",
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
class LockerForm(ModelForm):
    class Meta:
        model = Locker
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username','ploeg','locker', 'email', 'bio']
