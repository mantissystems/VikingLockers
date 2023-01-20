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

# def getKluizenList(request):
#     kluisjes = Kluis.objects.all()
#     serializer = KluisSerializer(kluisjes, many=True)
#     return Response(serializer.data)

# def updateNote(request, pk):
#     data = request.data
#     note = Note.objects.get(id=pk)
#     serializer = NoteSerializer(instance=note, data=data)

#     if serializer.is_valid():
#         serializer.save()

#     return serializer.data


# def deleteNote(request, pk):
#     note = Note.objects.get(id=pk)
#     note.delete()
#     return Response('Note was deleted!')

def getKluizenList(request):
    kluisjes = Note.objects.all()
    serializer = NoteSerializer(kluisjes, many=True)
    return Response(serializer.data)

#     if serializer.is_valid():
#         serializer.save()

#     return serializer.data


# def deleteKluis(request, pk):
#     note = Kluis.objects.get(id=pk)
#     note.delete()
#     return Response('Kluis was deleted!')