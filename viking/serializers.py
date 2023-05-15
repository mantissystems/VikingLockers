from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import   Note,KluisjesRV,Vikinglid
from django.contrib.auth.models import User


# class TopicSerializer(ModelSerializer):
#     class Meta:
#         model = Topic
#         fields = '__all__'

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

# class ActiviteitSerializer(ModelSerializer):
#     lid_van = serializers.PrimaryKeyRelatedField(queryset=Vikinglid.objects.all(), many=True)
#     class Meta:
#         model = Activiteit
#         fields = '__all__'

class KluisSerializer(ModelSerializer):
    class Meta:
        model = KluisjesRV
        fields = '__all__'
        
class GebruikerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_name')

