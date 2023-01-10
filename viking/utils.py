from rest_framework.response import Response
from .models import Note,Kluis
from .serializers import NoteSerializer,KluisSerializer


def getNotesList(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


def getNoteDetail(request, pk):
    notes = Kluis.objects.get(id=pk)
    serializer = KluisSerializer(notes, many=False)
    return Response(serializer.data)


def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

def updateNote(request, pk):
    data = request.data
    note = Kluis.objects.get(id=pk)
    serializer = KluisSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer.data


def deleteNote(request, pk):
    note = Kluis.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')

def getKluizenList(request):
    kluisjes = Kluis.objects.all()
    serializer = KluisSerializer(kluisjes, many=True)
    return Response(serializer.data)

def getKluisDetail(request, pk):
    notes = Kluis.objects.get(id=pk)
    serializer = KluisSerializer(notes, many=False)
    return Response(serializer.data)


def createKluis(request):
    data = request.data
    note = Kluis.objects.create(
        body=data['body']
    )
    serializer = KluisSerializer(note, many=False)
    return Response(serializer.data)

def updateKluis(request, pk):
    data = request.data
    note = Kluis.objects.get(id=pk)
    serializer = KluisSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return serializer.data


def deleteKluis(request, pk):
    note = Kluis.objects.get(id=pk)
    note.delete()
    return Response('Kluis was deleted!')