from django.shortcuts import redirect, render
from viking.models import Topic, Matriks,KluisjesRV
from .models import Room,Message,User
from django.db.models import Q
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lockers=Matriks.objects.all() 
    matriks=Matriks.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).order_by('name')
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    for i in range (0,13):
        kopmtrx.append(hdr[i])
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 
               'topics': topics,
                'lockers': lockers,
                'kopmtrx': kopmtrx,
               'room_count': room_count, 
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    vikingers=User.objects.all()
    topic=room.name

    ftopic=Q(topic__icontains=topic)
    fverhuurd=Q(verhuurd=True)

    verhuurd=KluisjesRV.objects.all().filter(ftopic&fverhuurd)  #verzamel verhuurde kluisjes voor de room 

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    heren=Matriks.objects.filter(naam__icontains=topic).exclude(y_as__in=(7,8)).order_by('y_as')
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    for i in range (0,13):
        kopmtrx.append(hdr[i])
    topics = Topic.objects.all()[0:5]
    context = {
        'room': room,
               'topics': topics,
                'heren': heren,
                'verhuurd': verhuurd,
                'kopmtrx': kopmtrx,
               'participants': participants,
               'room_messages': room_messages}

    return render(request, 'base/room.html', context)
