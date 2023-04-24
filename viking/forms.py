from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Kluis, User,Vikinglid,Activiteit,KluisjesRV
from django.forms.widgets import DateInput, NumberInput
from django.forms.fields import MultipleChoiceField

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'

class Urv_KluisForm(ModelForm):
    class Meta:
        model = Activiteit
        fields = '__all__'

class KluisjeForm(ModelForm):
    class Meta:
        model = KluisjesRV
        # model=Kluis
        fields = '__all__'

class VikinglidForm(ModelForm):
    class Meta:
        model = Vikinglid
        fields = '__all__'
        def __init__(self, *args, **kwargs):
            self.fields['is_lid_van'].queryset=Vikinglid.objects.filter(id=self.id)
            self.fields['is_lid_van'].widget.attrs.update(size='20')

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'email']        
