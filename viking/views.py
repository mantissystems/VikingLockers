from time import strftime
from urllib import request
from django.shortcuts import render
import datetime
from datetime import date
from django.utils import timezone
from django.http import HttpResponse,JsonResponse
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from viking.models import( Flexevent,Flexlid,Instromer,
Person,)
from collections import namedtuple
from django.db import connection
from django.views.generic import(ListView,UpdateView,DetailView)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from viking.serializers import FlexrecurrentSerializer, PersoonSerializer, TopicSerializer ,GebruikerSerializer
from .models import Bericht, Flexrecurrent, Message, Room, Topic,Kluis
from .forms import RoomForm,UserForm,Urv_KluisForm

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name or password does not exist')

    context = {'page': page}
    return render(request, 'viking/login_register.html', context)

def erv_loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'User name or password does not exist')

    context = {'page': page}
    return render(request, 'viking/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False) # commit=False : for get the user (for email lower case)
            user.username = user.username.lower()
            user.save()

            # log the user in
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'Error occurred during registration.')

    context = {'form': form}
    return render(request, 'viking/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    where1=Q(topic__name__icontains = q)
    where2=Q(topic__name__icontains = q)
    where3=Q(name__icontains = q)
    where4=Q(description__icontains = q)
    where5=Q(host__last_name__icontains = q) 
    # where1=Q(participants__last_name__icontains = q)
    rooms = Room.objects.filter(where1|where2|where3|where4|where5)
        # ) #.exclude(participants=None) # search 
    topcs = Topic.objects.all()
    rms = Room.objects.all().exclude(id__in=(87,88))
    participants_count=0
    kastjes_count=0
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        messages.error(request, '.U bent niet ingelogd waardoor gegevens niet getoond worden')

    if q=='kluisjes' :
        # print(q)
        lijst='kluisjes'
        kstn = Kluis.objects.all().filter(owners=None)
        for k in kstn:
            kk=k.owners.all()
            kastjes_count+=kk.count()

    else:
        lijst='ploegen'
        kstn = Kluis.objects.none
        kstn = Kluis.objects.filter(
        Q(name__icontains = q) | 
        Q(location__icontains = q) |
        Q(location__icontains = 'dames') |
        Q(location__icontains = 'heren') 
        ) #.exclude(owners=None) # search 
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    for rm in rms:
        rr=rm.participants.all()
        participants_count+=rr.count()
    # print(kstn)
    context = {
        'rooms': rooms, 
        'kluisjes': kstn, 
        'lijst': lijst, 
        'topics': topcs, 
        'room_count': room_count, 
        'participants_count': participants_count, 
        'kastjes_count': kastjes_count, 
        'room_messages': room_messages
        }
    return render(request, 'viking/home.html', context)

def erv_home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all() ##.filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = month # int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    usr=request.user
    users=User.objects.all()
    aangemelden=Person.objects.all().filter(id__in=users)
    flexevents = Flexevent.objects.all().filter(
        Q(lid__count__gt=0) & 
        # Q(datum__range=[start, end]) & 
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) | 
        Q(event_text__icontains = q) | 
        Q(description__icontains = q) 
        ) # search 
    d=[]
    ll=[]
    sc1=[]
    sc2=[]
    sc3=[]
    for fl in flexevents:
        ll=fl.lid.all()
        ll | ll
    aangemeld=ll
    # print(ll)
    aangemeld=User.objects.all().filter(
    Q(id__in=aangemeld)
        )
    room_count = flexevents.count()
    # namen=Person.objects.all()
    rooster=Flexevent.objects.all().filter(created__range=[start, end])
    context = {
        'rooster':rooster,
        'events': flexevents[0:6],   #te saneren in 3 templates
        'rooms': flexevents.all(), #[0:6],    #te saneren in 3 templates
        'deelnemers':aangemeld,    #alle deelnemers en hun skills
        'topics': topcs [0:6], 
        'room_count': room_count, #te saneren in 3 templates
        'room_messages': room_messages, #te saneren in 3 templates
        'sc1':aangemelden,
        }
    if 'viking' in q:
        redirect('aanmelden')            
        return render(request, 'viking/maand_list.html', context)

    return render(request, 'viking/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        messages.error(request, '.You are not logged in')

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'viking/room.html', context)
    
def erv_room(request, pk):
    event = Flexevent.objects.get(id=pk)
    event_messages = event.bericht_set.all()
    deelnemers = event.lid.all()
    kandidaten=User.objects.all().exclude(id__in=deelnemers)
    try:
        gebruiker=User.objects.get(id=request.user.id) ## request.user
    except:
        messages.error(request, '.You are not logged in')
        # print(request.user)
        context = {'event': event,
     'event_messages': event_messages, 
     'deelnemers': deelnemers,
     'kandidaten': kandidaten,
     }   
        return render(request, 'viking/room.html', context)
    if request.method == 'POST':
        gebruiker=User.objects.get(id=request.user.id) ## request.user
        bericht = Bericht.objects.create(
        user=gebruiker,
        event=event,
        body=request.POST.get('body')
        )
        return redirect('room', pk=event.id)
        # event.deelnemers.add(request.user)

    context = {'event': event,
     'event_messages': event_messages, 
     'deelnemers': deelnemers,
     'kandidaten': kandidaten,
    }
    return render(request, 'viking/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'viking/profile.html', context)
def erv_userProfile(request, pk):
    user = User.objects.get(id=pk)
    events = user.flexevent_set.all()[0:5]
    room_messages = user.message_set.all()
    topics = Topic.objects.all()    
    print(user)
    topcs = Topic.objects.all() #.filter(id__in=tops)
    topics = topcs
    context = {
        'user': user, 
        'events': events, 
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'viking/profile.html', context)
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'viking/room_form.html', context)

@login_required(login_url='login')
def erv_createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    datums=Flexevent.objects.all() ###values_list('datum',flat=True)
    # print(datums.datum)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        tijdstip=request.POST.get('tijdstip')
        activiteit = request.POST.get('topic')
        omschrijving=request.POST.get('description')
        datum=request.POST.get('datum')
        plandatum = datum #.strftime("%m/%d/%Y")

        omschrijving=plandatum + '; ' + activiteit
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Flexevent.objects.create(
             host=request.user,
            topic=topic,
            pub_time=request.POST.get('tijdstip'),
            name = request.POST.get('topic'),
            description=omschrijving, ##request.POST.get('description'),
            datum=request.POST.get('datum'),
            event_text=topic,
            # flexhost=request.user,

        )
        return redirect('home')
    context = {'form': form, 'topics': topics,'datums':datums}
    return render(request, 'viking/flexevent_form.html', context)

# @login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    ploegleiders=User.objects.all()
    # if request.user != room.host:
        # return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        ploegleider=request.POST.get('ploegleider')
        try:
            host=User.objects.get(last_name=ploegleider)
        except:
            host=User.objects.get(is_superuser=True)
        room.host = host
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room,'ploegleiders':ploegleiders}
    return render(request, 'viking/room_form.html', context)

@login_required(login_url='login')
def urv_updateKluis(request, pk):
    kluis = Kluis.objects.get(id=pk)
    form = Urv_KluisForm(instance=kluis)
    topics = Topic.objects.all()
    # if request.user != kluis.user:
    #     return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        # topic_name = request.POST.get('topic')
        # topic, created = Topic.objects.get_or_create(name=topic_name)
        # kluis.created=date.today()
        kluis.name = request.POST.get('name')
        kluis.code = request.POST.get('code')
        kluis.slot = request.POST.get('slot')
        kluis.description = request.POST.get('description')
        kluis.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'kluis': kluis}
    return render(request, 'viking/kluis_form.html', context)

@login_required(login_url='login')
def erv_deleteRoom(request, pk):

    room = Flexevent.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'viking/delete.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'viking/delete.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):

    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'viking/delete.html', context)

@login_required(login_url='login')
def erv_deleteMessage(request, pk):

    message = Bericht.objects.get(id=pk)

    # if request.user != message.user:
    #     return HttpResponse('Geen toestemming. Het is niet uw bericht!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'viking/delete.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'viking/update-user.html', {'form': form})

@login_required(login_url='login')
def erv_updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'viking/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'viking/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'viking/activity.html', {'room_messages': room_messages})

def erv_activityPage(request):
    tops=Flexevent.objects.values_list('topic', flat=True)
    topcs = Topic.objects.all().filter(id__in=tops)
    room_messages = Bericht.objects.all() ##filter(Q(room__topic__name__icontains=q))
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    beginmonth = 1 #int(date.today().strftime('%m'))
    endmonth = 12 # int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
    einde=monthend[endmonth]
    start=date(year,beginmonth,1)
    end=date(year,month,einde)
    usr=request.user
    users=User.objects.all()
    aangemelden=Person.objects.all().filter(id__in=users)

    flexevents = Flexevent.objects.all().filter(
        Q(datum__range=[start, end]) 
        ) # search 
    ff=Flexevent.objects.none()
    for fl in flexevents:
        ff = fl.lid.all()
        ff | ff
    deelnemers = ff
    aangemeld=deelnemers
    skills=Person.objects.all().filter(
        Q(id__in=aangemeld) &
        Q(pos1__in=['sc1','sc2','sc3'])&
        Q(pos2__in=['sc1','sc2','sc3'])&
        Q(pos3__in=['sc1','sc2','sc3'])&
        Q(pos4__in=['sc1','sc2','sc3'])&
        Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
        )
    room_count = flexevents.count()
    sc1=Person.objects.all().filter(
        Q(id__in=aangemeld) &
        Q(pos1__in=['sc1'])&
        Q(pos2__in=['sc1'])&
        Q(pos3__in=['sc1'])&
        Q(pos4__in=['sc1'])&
        Q(pos5__in=['st1','st2','st3'])  #pos5 = stuur
        )
    room_count = flexevents.count()
    rooster=Flexevent.objects.all().filter(datum__range=[start, end])

    context = {
        'events': flexevents,
        'rooms': flexevents, 
        'personen':skills,
        'topics': topcs, 
        'room_count': room_count, 
        'sc1':aangemelden,
        'room_messages': room_messages
        }

    return render(request, 'viking/activity.html', context)

def erv_topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Flexevent.objects.filter(name__contains=q)[0:6] ##.values_list('topic', flat=True)
    # topcs = Topic.objects.all().filter(id__in=tops)
    # topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'viking/topics.html', {'topics': topics})

def PloegPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.all().filter(name__contains=q) #.exclude(participants=None)
    # topcs = Topic.objects.all().filter(id__in=tops)
    # topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'viking/ploeg_list.html', {'rooms': rooms})

def KluisPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    kluisjes=Kluis.objects.all().filter(name__contains=q) #.exclude(participants=None)
    return render(request, 'viking/kluis_list.html', {'kluisjes': kluisjes})

class FlexeventsView(ListView):
    queryset=Flexevent.objects.all()
    
    def get_context_data(self, **kwargs):

        sl_ = self.kwargs.get("slug")
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        beginmonth = 1 #int(date.today().strftime('%m'))
        endmonth = 12 # int(date.today().strftime('%m'))
        # if beginmonth != 12:endmonth=beginmonth+1
        print(beginmonth,endmonth)
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[endmonth]
        x=0
        start=date(year,beginmonth,1)
        end=date(year,month,einde)
        x=10
        # rooster=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        rooster=Flexevent.objects.all()[:x]
        # print(rooster)
        for r in rooster:
            aanwezig=Flexlid.objects.all().filter(flexevent_id=r.id)
            ingedeelden=aanwezig.values_list('member_id', flat=True)
            # print(len(aanwezig))
            x+=len(aanwezig)
        y=int(x/4)
            # y=8
        roostergedeeltelijk=Flexevent.objects.filter(pub_date__range=[start, end])[:x]
        context = {
        'rooster': rooster,
        'roostergedeelte': roostergedeeltelijk,
        'events': roostergedeeltelijk,
        'regels':y,
        } 
        return context


@api_view(['GET'])
def personenlijst(request):
    deelnemers=Person.objects.all()
    serializer=PersoonSerializer(deelnemers,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def gebruikerslijst(request):
    gebruikers=User.objects.all()
    serializer=GebruikerSerializer(gebruikers,many=True)

    return Response(serializer.data)

@api_view(['GET'])
def aantalregels(request):
    regels=Flexrecurrent.objects.all()
    serializer=FlexrecurrentSerializer(regels,many=True)

    return Response(serializer.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


@api_view(['GET'])
def activiteit(request,pk):
    topic=Flexevent.objects.get(id=pk)

    serializer=TopicSerializer(topic,many=False)
    # if serializer.is_valid():
    #     serializer.save()

    return Response(serializer.data)

# @api_view(['DELETE'])
# def bootWerfuit(request,pk):
#     boot=Boot.objects.get(id=pk)
#     boot.delete()
    
#     return Response('boot verwijderd uit de werf')


class DetailView(DetailView):
    model = Flexevent
    template_name = 'viking/detail.html'
    def get_context_data(self, **kwargs):

        sl_ = self.kwargs.get("pk")
        zoeknaam=self.kwargs.get("zoeknaam")
        event=Flexevent.objects.get(id=sl_)
        aanwezig=Flexlid.objects.all().filter(flexevent_id=event.id)
        aangemeld=event.lid.all()
        # ingedeelden=aanwezig.values_list('member_id', flat=True)
        kandidaten=User.objects.all().exclude(id__in=aangemeld)
        aanwezigen=User.objects.all().filter(id__in=aangemeld)
        print(sl_,zoeknaam)
        context = {
            'event':event,
        # 'aanwezig': ingedeelden,
        'kandidaten': kandidaten,
        'aanwezig': aanwezigen,
        } 
        return context

class ResultsView(DetailView):
    model = Flexevent
    template_name = 'viking/room.html'
    def get_context_data(self, **kwargs):
        sl_ = self.kwargs.get("pk")
        flexevent=Flexevent.objects.filter(id=sl_)
        # print(flexevent)
        context = {
        'flexevent':flexevent,
        } 
        return context

def vote(request, room_id):
    event = get_object_or_404(Room, pk=room_id)
    zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else 'sc'
    # print('event: ', event,'zoeknaam: ', zoeknaam)

    leden = []
    afmeldingen=[]
    for af in request.POST.getlist('afmelding'):
        event.participants.remove(af)
    for l in request.POST.getlist('aanmelding'):
        event.participants.add(l)
    # for l in leden:
    #     try:
    #         uu=User.objects.get(id=l)
    #     except (KeyError, User.DoesNotExist):
    #         print('vote deelnemer add, except')
    personen=User.objects.all()
    kandidaten = User.objects.all().filter(
        Q(last_name__icontains = zoeknaam) | 
        Q(first_name__icontains = zoeknaam) 
        ).order_by('last_name') # search 
        # Q(person__pos1__icontains=zoeknaam) |
        # Q(person__pos1__icontains='sc') |
        # Q(person__pos2__icontains=zoeknaam) |
        # Q(person__pos3__icontains=zoeknaam) |
        # Q(person__pos4__icontains=zoeknaam) |
        # Q(person__pos5__icontains=zoeknaam)
    aangemeld=event.participants.all()
    aanwezigen=User.objects.all().filter(id__in=aangemeld)
    roeiers=Person.objects.filter(
        Q(id__in=aanwezigen) &
        Q(pos1__icontains=zoeknaam)
        )
    aantalregels=4
    # except (KeyError, Flexlid.DoesNotExist):
        # print(len(kandidaten)) ###regel niet verwijderen ###
    return render(request, 'viking/urv-detail.html', {
            'event': event,
            'users': personen,
            'roeiers': roeiers,
            'kandidaten':kandidaten,
            'aanwezig':aanwezigen, 
            'aantalregels':aantalregels,            
            'error_message': "Er is geen keuze gemaakt.",
        })
    print('vote room_id, else')
        # selected_choice.keuzes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('vote', args=(room_id,)))



def kluis(request, kluis_id):
    kluis = get_object_or_404(Kluis, pk=kluis_id)
    zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else 'sc'

    leden = []
    afmeldingen=[]
    for af in request.POST.getlist('afmelding'):
        kluis.owners.remove(af)
    for l in request.POST.getlist('aanmelding'):
        kluis.owners.add(l)
    personen=User.objects.all()
    kandidaten = User.objects.all().filter(
        Q(last_name__icontains = zoeknaam) | 
        Q(first_name__icontains = zoeknaam) 
        ) 
    aangemeld=kluis.owners.all()
    aanwezigen=User.objects.all().filter(id__in=aangemeld)
    roeiers=Person.objects.filter(
        Q(id__in=aanwezigen) &
        Q(pos1__icontains=zoeknaam)
        )
    return render(request, 'viking/urv-kluis-detail.html', {
            'kluis': kluis,
            'users': personen,
            'roeiers': roeiers,
            'kandidaten':kandidaten,
            'aanwezig':aanwezigen, 
            'error_message': "Er is geen keuze gemaakt.",
        })
    print('kluis room_id, else')
        # selected_choice.keuzes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('kluis', args=(kluis_id,)))



class AanmeldView(ListView):
    template_name='viking/aanmeldview.html'
    # print('aanmelden')
    queryset=Flexevent.objects.all()
    def get_context_data(self, **kwargs):
        x=0
        year=int(date.today().strftime('%Y'))
        month = int(date.today().strftime('%m'))
        volgendemaand=month
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        x+=1
        if month <= 12 and x==0: volgendemaand=month+1
        einde=monthend[volgendemaand]
        end=date(year,month,einde)
        beginmonth = 1 #int(date.today().strftime('%m'))
        endmonth = 12 # int(date.today().strftime('%m'))
        monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
        einde=monthend[endmonth]
        # aantalregels=10
        start=date(year,beginmonth,1)
        end=date(year,endmonth,einde)
        start=date(year,beginmonth,1)
        rooster=Flexevent.objects.filter(datum__range=[start, end])
        roostergedeeltelijk=Flexevent.objects.filter(datum__range=[start, end])
        context = {
        'rooster': rooster,
        } 
        return context


def events(request):
    q1 = Flexevent.objects.all()
    print('events')
    # fp = Flexevent.objects.filter(id=1).values('flexpoule')[0:1]
    r = q1
    template_name = 'viking/maand_list.html'
    aanwezigen = Flexlid.objects.all() #values_list('member_id', flat=True).filter(is_present=True)
    events = Flexevent.objects.all() #.filter(flexhost='',flexhost2='')
    rowers = Person.objects.all() #.filter(is_present=True)
    hosts = Person.objects.all() #.filter(is_host=True)
    rowers = rowers | hosts  # voeg hosts en roeiers samen
    results=Flexevent.objects.all()
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    einde=monthend[month]
    start=date(year,month,1)
    end=date(year,month,einde)
    namen=Person.objects.all()
    rooster=Flexevent.objects.filter(datum__range=[start, end])
    print(month,einde,start,end,rooster)
    context={
        # 'object_list':results,
        'rooster':rooster,
        'namen':namen,
       }
    return render(request, template_name, context)



def recurrent_event(request):
    template_name = 'viking/home.html'

    # Topic.objects.all().delete()
    # Flexevent.objects.all().delete()
    # maak_activiteiten() #flexevents; houd tijdelijk niet qctief
    # update_ploegen()
    return render(request, template_name, {})

def update_ploegen():
    room=Room.objects.get(pk='93')
    room=Room.objects.get(pk='88')
    # heren=Kluis.objects.all().filter(location__icontains='Heren')
    heren=Kluis.objects.all().filter(location__icontains='Dames')
    usr=User.objects.none
    for kk in heren:
        usr=User.objects.get(pk=kk.user_id)
        room.participants.add(usr)
                
    return

def maak_rooms(tekst,gebruiker):
        eerste=Topic.objects.all().first()
        start_date = datetime.date.today()
        Flexevent.objects.all().update_or_create(
        host=gebruiker,
        topic=eerste,
        name=tekst,
        description='omschrijving',
        created=start_date,
        )
        return

def maak_activiteiten():
    start_date = datetime.date.today()
    # tomorrow = start_date + datetime.timedelta(days=1)
    dagnaam=datetime.datetime.now().strftime('%A')
    weekdag=datetime.datetime.now().strftime('%w')
    dagnummer=int(weekdag)
    day_delta = datetime.timedelta(days=1)
    for d in range(7):
        tomorrow = start_date + datetime.timedelta(days=d)
    weekdag=int(start_date.strftime('%w'))
    trainingsweken=4 ####45
    for j in range(trainingsweken):
        day_delta = datetime.timedelta(days=7) 
        datum2=start_date + j * day_delta   
        weekdag=datum2.strftime('%w')
        activiteit='training_' + str(j)
        week=datum2.strftime('%W')
        datum = datum2.strftime("%m/%d/%Y")
        user=User.objects.all().first()
        for t in range(1,7,1):
            topc=Topic.objects.create(name='training_' + str(t))
            tijd2="20:30"
            Flexevent.objects.all().update_or_create(
            event_text='training_' + str(t),
            name='training_' + str(t),
            description=dagnaam + '; ' + weekdag + '; ' + datum , 
            created=datum2,
            pub_time=tijd2,
            datum=datum2,
            host=user,
            topic=topc,
            )
        events=Flexevent.objects.all()
        gebruikers=User.objects.all()

        for f in events:
            for p in gebruikers:
                f.lid.add(p)

    return
@api_view(['GET'])
def apiOverview(request):
    api_urls={
    'api/':'api-overview',    
    'api/person':'api/person',    
    'api/gebruikers':'gebruikerslijst',    
    'flexevents/':'flexevents',    
    'flexeventsbeheer/':'flexeventsbeheer',    

    }
    # return JsonResponse("API BASE POINT",safe=False)
    return Response(api_urls)

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def ploeg_participants(request):
        
        sql="select * from ploeg_participants"
        cursor = connection.cursor() 
        cursor.execute(sql)
        results = namedtuplefetchall(cursor)
        usr=User.objects.first()
        print('===== ploeg-participants =====')
        for r in results:
            # print(r.Naamploeg)
            room=Room.objects.get(name=r.Naamploeg)
            instroom=Instromer.objects.none()
            # print(room) 
            if r.Ploegleden!=None:
                try:
                    usr=User.objects.get(last_name=r.Ploegleden)
                    room.participants.add(usr)
                except:
                    Instromer.objects.update_or_create(name=r.Ploegleden)

            if r.field3!=None:
                try:
                    usr=User.objects.get(last_name=r.field3)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field3)

                    context={}
            if r.field4!=None:
                try:
                    usr=User.objects.get(last_name=r.field4)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field4)

                    context={}
            if r.field5!=None:
                try:
                    usr=User.objects.get(last_name=r.field5)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field5)

                    context={}
            if r.field6!=None:
                try:
                    usr=User.objects.get(last_name=r.field6)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field6)

                    context={}
            if r.field7!=None:
                try:
                    usr=User.objects.get(last_name=r.field7)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field7)

                    context={}
            if r.field8!=None:
                try:
                    usr=User.objects.get(last_name=r.field8)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field8)

                    context={}
            if r.field9!=None:
                try:
                    usr=User.objects.get(last_name=r.field9)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field9)
                    context={}
            if r.field10!=None:
                try:
                    usr=User.objects.get(last_name=r.field10)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field10)
                    context={}
            if r.field11!=None:
                try:
                    usr=User.objects.get(last_name=r.field11)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field11)

                    context={}
            if r.field12!=None:
                try:
                    usr=User.objects.get(last_name=r.field12)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field12)

                    context={}
            if r.field13!=None:
                try:
                    usr=User.objects.get(last_name=r.field13)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field13)

                    context={}
            if r.field14!=None:
                try:
                    usr=User.objects.get(last_name=r.field14)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field14)
                    context={}
            if r.field15!=None:
                try:
                    usr=User.objects.get(last_name=r.field15)
                    room.participants.add(usr)                    
                except:
                    Instromer.objects.update_or_create(name=r.field15)
                    context={}
    #     'hoofdletters':results,
    #     'object_list':results,
    #    }
        return HttpResponse('done')
