from rest_framework.serializers import ModelSerializer
from base.models import Bericht


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Bericht
        fields = '__all__'
