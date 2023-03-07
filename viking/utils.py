from rest_framework.response import Response
from .models import Note,Kluis
from .serializers import NoteSerializer,KluisSerializer


def getNotesList(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def getNoteDetail(request, pk):
    notes = Note.objects.get(id=pk)
    serializer = NoteSerializer(notes, many=False)
    return Response(serializer.data)

def getKluizenList(request):
    kluisjes = Note.objects.all()
    serializer = NoteSerializer(kluisjes, many=True)
    return Response(serializer.data)
