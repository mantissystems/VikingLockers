from rest_framework import serializers
from .models import Flexevent, Room, Person, Topic
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
        model = Room
        fields='__all__'        
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flexevent
        fields='__all__'                

class GebruikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_name')

# importing the module
import json

# opening the JSON file
# data = open('file.json',)

# print("Datatype before deserialization : "
# 	+ str(type(data)))
	
# # deserializing the data
# data = json.load(data)

# print("Datatype after deserialization : "
# 	+ str(type(data)))

