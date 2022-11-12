from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Kluis, Room,User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
    #   fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['participants']

class Urv_KluisForm(ModelForm):
    class Meta:
        model = Kluis
        fields = '__all__'
        exclude = ['host','owners']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'email']        
        # fields = ['avatar', 'name', 'username', 'email', 'bio']        