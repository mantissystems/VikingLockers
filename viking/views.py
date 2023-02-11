import random
from array import *
from time import strftime
from urllib import request
from django.shortcuts import render
import datetime
import itertools
from datetime import date
from django.utils import timezone
from django.http import HttpResponse,JsonResponse,response
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse,reverse_lazy
from viking.models import( Instromer,Person,)
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

from viking.serializers import FlexrecurrentSerializer,  PersoonSerializer,  GebruikerSerializer,KluisSerializer,NoteSerializer
from .models import Flexrecurrent, Message, Room, Topic,Kluis,Rooster,Vikinglid,Activiteit,Note
from .forms import RoomForm,UserForm,Urv_KluisForm,VikinglidForm
from .utils import (getNoteDetail, getNotesList,)

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
    topcs = Activiteit.objects.values('type') .filter(name__icontains=q)
    topics = Topic.objects.all()
    all=Vikinglid.objects.all()
    empty=[]
    filter1=Q(name__icontains=q)    
    vikingleden=Vikinglid.objects.all().filter(filter1 )

    if q=='Kluisjes-leeg':
        for z in all:
            kl=z.is_lid_van.all()
            act=Activiteit.objects.values_list('name',flat=True).filter(lid_van__id=z.id)
            if act: 
                k=kl.values_list('id',flat=True)
                # print(k)
                empty.append(k)
        vikingleden=Vikinglid.objects.all().filter(id__in=empty)

    if q=='Kluisjes-bezet':
        print(q)
        vikingleden=Vikinglid.objects.all()
    vl=Vikinglid.objects.all().filter(is_lid_van__name__icontains=q)
    if vl and len(q)>0: 
        print('vl',q,'vl', vl.count())
        vikingleden=Vikinglid.objects.all().filter(is_lid_van__name__icontains=q)
    context = {
        'vikingleden':vikingleden,
        'topics': topics, 
        'topcs':topcs,
        'empty':empty,
        'q':q,
        }
    return render(request, 'viking/home.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    kluis = Kluis.objects.get(id=pk)
    participants = room.participants.all()
    owners=kluis.owners.all()

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

    context = {'room': room, 'room_messages': room_messages, 'participants': participants,'owners': owners}
    return render(request, 'viking/room.html', context)
    
# def erv_room(request, pk):
#     # event = Flexevent.objects.get(id=pk)
#     # event_messages = event.bericht_set.all()
#     # deelnemers = event.lid.all()
#     # kandidaten=User.objects.all().exclude(id__in=deelnemers)
#     try:
#         gebruiker=User.objects.get(id=request.user.id) ## request.user
#     except:
#         messages.error(request, '.You are not logged in')
#         # print(request.user)
#         context = {'event': event,
#      'event_messages': event_messages, 
#      'deelnemers': deelnemers,
#      'kandidaten': kandidaten,
#      }   
#         return render(request, 'viking/room.html', context)
#     if request.method == 'POST':
#         gebruiker=User.objects.get(id=request.user.id) ## request.user
#         bericht = Bericht.objects.create(
#         user=gebruiker,
#         event=event,
#         body=request.POST.get('body')
#         )
#         return redirect('room', pk=event.id)
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
def createVikinglid(request):
    form = VikinglidForm()
    topics = Activiteit.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('islidvan')
        email = request.POST.get('email')
        print(email)
        # topic, created = Topic.objects.get_or_create(name=topic_name)
        vikinglid=Vikinglid.objects.create(
            email=email,
            avatar='avatar.svg',
            name=request.POST.get('name'),
        )
        print(vikinglid.id)
        return redirect('home')
    vikinglid=Vikinglid.objects.all().last()

    context = {'form': form, 'topics': topics, 'vikinglid':vikinglid}
    return render(request, 'viking/vikinglid_form.html', context)

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
    vikinglid=Vikinglid.objects.get(id=pk)
    form=VikinglidForm(instance=vikinglid)
    kluizen=Activiteit.objects.all().filter(type='kluis').order_by('name')
    teams=Activiteit.objects.all().filter(type='ploeg').order_by('name')
    lidvan = vikinglid.is_lid_van.all()
    if request.method == 'POST':
        for team in request.POST.getlist('is_lid_van'):
            vikinglid.is_lid_van.add(team)
            print(team)
        for kluis in request.POST.getlist('heeftkluis'):
            vikinglid.is_lid_van.add(kluis)
            vikinglid.is_lid_van.add(kluis)
            print(kluis)
        vikinglid.name = vikinglid.name
        vikinglid.name = request.POST.get('name')
        vikinglid.email = request.POST.get('email')
        vikinglid.save()
        return redirect('home')

    # context = {'form': form, 'topics': topics, 'vikinglid': vikinglid}
    context = {
        'form': form,
          'vikinglid': vikinglid,
          'lidvan':lidvan,
          'kluizen':kluizen,
          'teams':teams,
    }
    return render(request, 'viking/vikinglid_form.html', context)

@login_required(login_url='login')
# def erv_deleteRoom(request, pk):

#     room = Flexevent.objects.get(id=pk)

#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!!')

#     if request.method == 'POST':
#         room.delete()
#         return redirect('home')

#     context = {'obj': room}
#     return render(request, 'viking/delete.html', context)

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
def deleteVikinglid(request, pk):

    vikinglid = Vikinglid.objects.get(id=pk)

    # if request.user != room.host:
    #     return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        vikinglid.delete()
        return redirect('home')

    context = {'obj': vikinglid}
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
# def erv_deleteMessage(request, pk):

#     message = Bericht.objects.get(id=pk)

#     # if request.user != message.user:
#     #     return HttpResponse('Geen toestemming. Het is niet uw bericht!!')

#     if request.method == 'POST':
#         message.delete()
#         return redirect('home')

#     context = {'obj': message}
#     return render(request, 'viking/delete.html', context)

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
    topics = Activiteit.objects.filter(name__icontains=q)
    return render(request, 'viking/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'viking/activity.html', {'room_messages': room_messages})


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

# @api_view(['GET', 'POST'])
# def getNotes(request):

#     if request.method == 'GET':
#         return getNotesList(request)

#     if request.method == 'POST':
#         return createNote(request)

# @api_view(['GET'])
# def kluisjes(request):
#     kluizen=Kluis.objects.all()
#     serializer=KluisSerializer(kluizen,many=True)

#     return Response(serializer.data)

def get_vikinglid(request):
    template_name = 'viking/vikinglid.html'

    vikingleden=Vikinglid.objects.all() ##.filter(name__in=('zaterdag','zondag'))
    context={'vikingleden':vikingleden}
    return render(request, template_name, context)

@login_required(login_url='login')
def add_activity(request):
    # add kluis and ploeg to vikinglid.
    # kluis through user,kluis; ploeg kluis where sleutels=vikinglid (2=leeg); code==activiteit
    vikingleden=Vikinglid.objects.all()
    kluisjes=Kluis.objects.all()
    for k in kluisjes:
        vl=Vikinglid.objects.get(id=k.sleutels)
        act=Activiteit.objects.get(id=k.code)
        vl.is_lid_van.add(act)
    context={
        'vikingleden':vikingleden,
        # 'lege_kastjes_count':vl.count(),
            # 'vikinglid': vikinglid,
            # 'users': personen,
            'error_message': "Er is geen keuze gemaakt.",
        }

    return render(request, 'viking/vikinglid.html', context)

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


@login_required(login_url='login')
def kluis(request, kluis_id):
    kluis = get_object_or_404(Vikinglid, pk=kluis_id)
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
        Q(id__in=aanwezigen)
        # Q(pos1__icontains=zoeknaam)
        )
    return render(request, 'viking/vikinglid-detail.html', {
            'kluis': kluis,
            'users': personen,
            'roeiers': roeiers,
            'kandidaten':kandidaten,
            'aanwezig':aanwezigen, 
            'error_message': "Er is geen keuze gemaakt.",
        })
    return HttpResponseRedirect(reverse('kluis', args=(kluis_id,)))

@login_required(login_url='login')
def activiteit(request, lid_id):
    vikinglid = get_object_or_404(Vikinglid, pk=lid_id)
    zoeknaam = request.POST.get('zoeknaam') if request.POST.get('zoeknaam') != None else ''
    print(lid_id)
    leden = []
    afmeldingen=[]
    for af in request.POST.getlist('afmelding'):
        vikinglid.is_lid_van.remove(af)
    for l in request.POST.getlist('aanmelding'):
        vikinglid.is_lid_van.add(l)
    personen=User.objects.all()
    kandidaten = Activiteit.objects.all().filter(
        Q(name__icontains = zoeknaam) | 
        Q(type__icontains = zoeknaam) 
        ) [0:10]
    islidvan=vikinglid.is_lid_van.all()
    aanwezigen=Activiteit.objects.all().filter(id__in=islidvan)
    roeiers=Person.objects.filter(
        Q(id__in=aanwezigen)
        # Q(pos1__icontains=zoeknaam)
        )
    return render(request, 'viking/vikinglid-detail.html', {
            'vikinglid': vikinglid,
            'users': personen,
            'roeiers': roeiers,
            'kandidaten':kandidaten,
            'islidvan':islidvan, 
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
    # queryset=Flexevent.objects.all()
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
        # rooster=Flexevent.objects.filter(datum__range=[start, end])
        # roostergedeeltelijk=Flexevent.objects.filter(datum__range=[start, end])
        context = {
        # 'rooster': rooster,
        } 
        return context

def personen():
    persoon=Person.objects.none()
    # rooster=Rooster.objects.all().update(rnr=0) #zet alle rangnummers op nul
    rooster=Rooster.objects.all().exclude(rnr=0)
    print(rooster.count())
    for dag in rooster:
            rangnr=getattr(dag, 'rnr')
            try:
                p=Person.objects.get(lnr=rangnr)
                uid=getattr(p, 'user_id')
                gebruiker=User.objects.get(id=uid)
                userid=getattr(p, 'user_id')
                try:
                    user=User.objects.get(id=userid)
                    dag.lid.add(user)
                except:
                    print()
                # print(gebruiker)
            except:
                print()
                # p=Person.objects.get(lnr=rangnr)
                # uid=getattr(p, 'user_id')

    return
def randomiseren():
    members=Person.objects.values_list('lnr','name','user_id')
    T=members
    lotingen=[]
    # rooster=Rooster.objects.all().update(rnr=0) #zet alle rangnummers op nul
    rooster=Rooster.objects.all()
    num1 =365 ## 54  ;aantal roosterregels 
    # num2 =members.count() ## 24  ;aantal members
    num3=136145  #lcm of num1 and num2; GGV van rooster en members
    # num4=random.randint(0, num1)
    # ======== 10 passes needed ============
    # for xx in range(12):
    for r in T:
        lot=random.randint(0, num1)
        try:
            rr=Rooster.objects.filter(
                Q(id=lot) &
                Q(rnr=0)).update(rnr=r[0]) #geef het rangnummer een gerandomiseerd nummer
            error: KeyError
            continue
        except:
            rr=Rooster.objects.filter(
                Q(id=lot) &
                Q(rnr=0)).update(rnr=r[0]) #geef het rangnummer een gerandomiseerd nummer    # start===== generate UNIQUE numbers and store once in PERSON ============ start

            # rr.lid.add(persoon)
    # Generate unique random numbers within a range (recordcount of rooster)
    # num_list = random.sample(range(0, recordcount-of-rooster), 10)
    # num_list = random.sample(range(0, num3), num2)
    # for i in range(1,num2,1):
    #     try:
    #         Person.objects.filter(id=i).update(lnr=num_list[i])
    #         error:KeyError
    #         continue
    #     except:
    #         Person.objects.filter(id=i).update(lnr=num_list[i])
    # end======= generate UNIQUE numbers and store once in PERSON ============ end
    # for ix, lnr in enumerate(members, start=1): 
        # lotingen.append(lnr[0])
        # T.insert(lnr[0], lnr[1])
        # print(lnr[0],lnr[1],lnr[2])
    # T.insert(2, [0,5,11,13,6])
    # print(T)
    # for m in members:
    # lnr=getattr(members, 'lnr') #to get the value from the model.
    # ===================== array start
    # ===================== array end
    return

def events(request):
    # personen()
    # for xx in range(12):
    #     randomiseren()

    members=Person.objects.values_list('lnr','name','user_id')
    # T=members
    # # T= [[1],['wb']]
    # lotingen=[]
    # rooster=Rooster.objects.all().update(rnr=0) #zet alle rangnummers op nul
    rooster=Rooster.objects.all()
    # num1 =365 ## 54  ;aantal roosterregels 
    # num2 =members.count() ## 24  ;aantal members
    # num3=136145  #lcm of num1 and num2; GGV van rooster en members
    # num4=random.randint(0, num1)
    # ======== 10 passes needed ============
    # for xx in range(12):
    #     for r in T:
    #         lot=random.randint(0, num1)
    #         # print(lot,r[0])
    #         try:
    #             rr=Rooster.objects.filter(
    #                 Q(id=lot) &
    #                 Q(rnr=0)).update(rnr=r[0]) #geef het rangnummer een gerandomiseerd nummer
    #             error: KeyError
    #             continue
    #         except:
    #             rr=Rooster.objects.filter(
    #                 Q(id=lot) &
    #                 Q(rnr=0)).update(rnr=r[0]) #geef het rangnummer een gerandomiseerd nummer    # start===== generate UNIQUE numbers and store once in PERSON ============ start

            # rr.lid.add(persoon)
    # Generate unique random numbers within a range (recordcount of rooster)
    # num_list = random.sample(range(0, recordcount-of-rooster), 10)
    # num_list = random.sample(range(0, num3), num2)
    # for i in range(1,num2,1):
    #     try:
    #         Person.objects.filter(id=i).update(lnr=num_list[i])
    #         error:KeyError
    #         continue
    #     except:
    #         Person.objects.filter(id=i).update(lnr=num_list[i])
    # end======= generate UNIQUE numbers and store once in PERSON ============ end
    # for ix, lnr in enumerate(members, start=1): 
        # lotingen.append(lnr[0])
        # T.insert(lnr[0], lnr[1])
        # print(lnr[0],lnr[1],lnr[2])
    # T.insert(2, [0,5,11,13,6])
    # print(T)
    # for m in members:
    # lnr=getattr(members, 'lnr') #to get the value from the model.
    # ===================== array start
    # ===================== array end
    template_name='viking/rooster_list.html'
    context={
        # 'object_list':results,
        'rooster':rooster,
        'namen':members,
       }
    return render(request, template_name, context)



@login_required(login_url='login')
def recurrent_event(request):
    template_name = 'viking/event_list.html'
    print('============ recurrent ============')
    # resetsequence('beatrix_flexevent')  # bestandsbeheer: zet sequence op nul; kan niet gelijktijdig
    # maak_activiteiten()
    maak_rooster()
    # events=Flexevent.objects.all()
    events=Rooster.objects.all()
    context={'events':events}
    return render(request, template_name, context)

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

def maak_rooster():
    print('====== start rooster ===========')
    Rooster.objects.all().delete()
    resetsequence('viking_rooster')  # bestandsbeheer: zet sequence op nul;
    start_date = datetime.date.today()
    user=User.objects.all().first()         ## -- de beheerder en superuser
    dagvandeweek=['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']
    for d in range(0,365,1):
        event_date = start_date + datetime.timedelta(days=d)       
            # Rooster.objects.all().update_or_create(
        Rooster.objects.all().create(
        host=user,
        datum=event_date,
        name=dagvandeweek[event_date.weekday()],
        description=dagvandeweek[event_date.weekday()],
        created=event_date,
        rnr=d,
        lnr=d,  #lotnummer wordt later toegekend
        )
    print('====== einde rooster ===========')
    return

def maak_activiteiten():
    start_date = datetime.date.today()
    tomorrow = start_date + datetime.timedelta(days=1)
    #hier moet het array komen met de voorkeur weekdagen; bijvoorbeeld maandag woensdag vrijdag
    #het schema alleen op de voorkeurdagen aanmaken
    #het eventuele bestaande schema op de voorkeurdagen aanpassen; dus datums manipuleren van alle regels
    # in het voorbeeld wil ik alleen op woensdag en vrijdag middag flexevents maken
    # de dagen zijn verdeeld in o en m en iederee o of m in twee blokken van 2 uur beginnend om 09 en om 13
    #0=monday
    #6=sunday
    # instellingen = Recurrent.objects.all().first()
    dagnaam=datetime.datetime.now().strftime('%A')
    weekdag=datetime.datetime.now().strftime('%w')
    dagnummer=int(weekdag)
    # model._meta.get_all_field_names()     will give you all the model's field names, then you can use 
    # dvdw=Recurrent._meta.get_field('dagvandeweek') #to work your way to the verbose name, and 
    blok=1 #getattr(instellingen, 'blok') #to get the value from the model.
    dvdw=6 #getattr(instellingen, 'dagvandeweek')
    bool0= False #getattr(instellingen, 'verwijder_oude_flexevents')
    bool1=False #getattr(instellingen, 'verwijder_oude_onderwerpen')
    bool2=True #getattr(instellingen, 'resetsequence')
    trw=4 #getattr(instellingen, 'trainingsweken')
    # print(blok,dvdw,trw,bool0,bool1,bool2)
    # return
    maak_alle_users_lid=False
    verwijder_oude_flexevents=True
    verwijder_oude_onderwerpen=False
    day_delta = datetime.timedelta(days=1)
    day_delta = datetime.timedelta(days=7) 
    year=int(date.today().strftime('%Y'))
    month = int(date.today().strftime('%m'))
    monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    einde=monthend[month]
    start=date(year,month,1)
    end=date(year,month,einde)
    trainingsweken=4 #kijk 4 weken vooruit - eigenlijk 45 trainingsweken
    user=User.objects.all().first()         ## -- de beheerder en superuser
    onderwerp='flexroeien: '
    week=[1,2,3,4,5,6,7]
    week=[1]
    dagvandeweek=['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag','7----','8====''maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag','16----','17====']
    blok=[0,1]                              #ochtend middag
    tijdblok=[' 09:00',' 13:00',' 17:30',' 09:00',' 13:00',' 17:30',' 09:00',' 13:00',' 17:30']   # 1x ochtend 2x middag
    # if verwijder_oude_flexevents: Flexevent.objects.all().delete()
    if verwijder_oude_onderwerpen: Topic.objects.all().delete()
        # resetsequence('beatrix_flexevent')  # bestandsbeheer: zet sequence op nul; kan niet gelijktijdig meet topics
    print('====== start ===========')
    i=1
    j=1
    return

def taak_rooster(request):
    template_name = 'viking/rooster_list.html'
    # print('============ recurrent ============')
    num1 =365 ## 54
    num2 =373 ## 24
    num3=136145  #lcm of num1 and num2
    num4=random.randint(0, num3)
    # Generate 10 unique random numbers within a range
    # num_list = random.sample(range(0, 1000), 10)
    # Generate unique random numbers within a range (recordcount of rooster)
    num_list = random.sample(range(0, num3), 365)
    # print(num_list)
    # Output [499, 580, 735, 784, 574, 511, 704, 637, 472, 211]    
    # print("The L.C.M. is", compute_lcm(num1, num2),num4)
    # events=Flexevent.objects.all()
    events=Rooster.objects.all() ##.filter(name__in=('zaterdag','zondag'))
    context={'rooster':events}
    return render(request, template_name, context)

@api_view(['GET'])
def apiOverview(request):
    api_urls={
    'api/':'api-overview',    
    '/kluizen':'kluizen',    
    '/notes/':'notes',    
    }
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
            room=Room.objects.get(name=r.Naamploeg)
            instroom=Instromer.objects.none()
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
def resetsequence(*args):        
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM sqlite_sequence");
    results = namedtuplefetchall(cursor)
    tabel='viking_rooster'
    sql="UPDATE sqlite_sequence SET seq =0 where name='" + tabel + "'"
    cursor.execute(sql)

# Python Program to find the L.C.M. of two input number
def compute_lcm(x, y):
   # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y
   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1
   return lcm
# num1 = 54
# num2 = 24
# print("The Lowest.Common.Meam. is", compute_lcm(num1, num2))

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getNote(request,pk):
    notes = Note.objects.get(id=pk)
    serializer = NoteSerializer(notes, many=False)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getNotes(request):
    notes = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def findNote(request,find):
    print(request,find)
    notes = Note.objects.all().order_by('-updated')
    if find is not None:
        notes = Note.objects.filter(body__icontains=find).order_by('-updated')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def updateNote(request, pk):
    data = request.data
    print(data)
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['GET','DELETE'])
def deleteNote(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Note was deleted!')

@api_view(['PUT','POST'])
def createNote(request):
    data = request.data
    note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)
