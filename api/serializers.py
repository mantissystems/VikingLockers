from rest_framework.serializers import ModelSerializer
from base.models import Bericht,Locker

class LockerSerializer(ModelSerializer):
    class Meta:
        model = Locker
        # fields=['locker']
        fields = '__all__'

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Bericht
        fields = '__all__'
