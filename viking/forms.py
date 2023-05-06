from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import  User,Vikinglid,KluisjesRV,Instromer
from django.forms.widgets import DateInput, NumberInput
from django.forms.fields import MultipleChoiceField
from django import forms

SLOT = [
            ('--', '--'),
            ('H', 'hang'),      #gebruiker heeft hangslot
            ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
            ]

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class InstromerForm(ModelForm):
    class Meta:
        model = Instromer
        fields = '__all__'

class KluisjeForm(ModelForm):
    class Meta:
        model = KluisjesRV
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            self.fields['type'] = forms.MultipleChoiceField(choices = SLOT)
            # self.fields['is_lid_van'].widget.attrs.update(size='20')

class VikinglidForm(ModelForm):
    class Meta:
        model = Vikinglid
        fields = '__all__'
        # def __init__(self, *args, **kwargs):
        #     self.fields['is_lid_van'].queryset=Vikinglid.objects.filter(id=self.id)
        #     self.fields['is_lid_van'].widget.attrs.update(size='20')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'email']        
