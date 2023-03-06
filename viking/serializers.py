from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Room,  Topic,Note,Kluis,Activiteit,Vikinglid
from django.contrib.auth.models import User


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
        
class GebruikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_name')

