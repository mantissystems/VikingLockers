from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Kluis, Room,User,Vikinglid,Activiteit
from django.forms.widgets import DateInput, NumberInput
from django.forms.fields import MultipleChoiceField

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

class VikinglidForm(ModelForm):
    class Meta:
        model = Vikinglid
        fields = '__all__'
        # exclude = ['is_lid_van']
        def __init__(self, *args, **kwargs):
            self.fields['is_lid_van'].queryset=Vikinglid.objects.filter(id=self.id)
            self.fields['is_lid_van'].widget.attrs.update(size='20')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'email']        
        # fields = ['avatar', 'name', 'username', 'email', 'bio']        