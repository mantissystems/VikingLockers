from rest_framework import serializers
from .models import Flexevent, Flexrecurrent, Person, Topic
from django.contrib.auth.models import User

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email')

class FlexeventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'
class FlexrecurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexrecurrent
        fields='__all__'        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'                

class GebruikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_name')
