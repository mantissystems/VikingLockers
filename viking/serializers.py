from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Room, Person, Topic,Note,Kluis,Activiteit,Vikinglid
from django.contrib.auth.models import User

class PersoonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name', 'email')

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class ActiviteitSerializer(ModelSerializer):
    lid_van = serializers.PrimaryKeyRelatedField(queryset=Vikinglid.objects.all(), many=True)
    class Meta:
        model = Activiteit
        fields = '__all__'

class KluisSerializer(ModelSerializer):
    class Meta:
        model = Kluis
        fields = '__all__'

class FlexrecurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields='__all__'        
        
class GebruikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_name')


# importing the module
# import json

# opening the JSON file
# data = open('file.json',)

# print("Datatype before deserialization : "
# 	+ str(type(data)))
	
# # deserializing the data
# data = json.load(data)

# print("Datatype after deserialization : "
# 	+ str(type(data)))

