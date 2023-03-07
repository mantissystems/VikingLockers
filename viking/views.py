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
# from viking.models import( Person,)
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

from viking.serializers import(
    GebruikerSerializer,
    KluisSerializer,
    NoteSerializer,
    ActiviteitSerializer,
)
from .models import   Topic,Kluis,Vikinglid,Activiteit,Note
from .forms import UserForm,Urv_KluisForm,VikinglidForm,KluisjeForm
# from .utils import (getNoteDetail, getNotesList,) 

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

def urv_loginPage(request):

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
    q = request.GET.get('q') if request.GET.get('q') != None else '' # 'Met Kluis'
    topcs = Activiteit.objects.values('type') .filter(name__icontains=q)
    template='viking/home.html'
    topics = Topic.objects.all()
    all=Vikinglid.objects.all()
    filter1=Q(name__icontains=q)    
    vikingleden=Vikinglid.objects.all().filter(filter1 )
    print('all', vikingleden.count())
    if q=='Aanvraag':
            return redirect('create-aanvrage')
    leeg = Activiteit.objects.all().filter(
        # Q(name=None) | 
        Q(type='kluis'))
    leeg = Activiteit.objects.all().filter(
        Q(name=None) | 
        Q(type='kluis'))
    billable = Activiteit.objects.none()
    vl=Vikinglid.objects.all().filter(is_lid_van__name__icontains=q)
    if vl and len(q)>0: 
        print('vl',q,'vl', vl.count())
        vikingleden=Vikinglid.objects.all().filter(is_lid_van__name__icontains=q)
    if q=='Kluisjes-leeg':
        template='viking/home.html'
        leeg = Activiteit.objects.all().filter(
        Q(lid_van=None) &
        Q(type='kluis')
        # Q(name='Wachtlijst')
        )
        print('leeg', leeg.count(),topcs)
    if q=='Met Kluis':
        billable = Activiteit.objects.all().exclude(
        Q(lid_van=None)| 
        Q(type='ploeg')
        # &
        )
        template='viking/home.html'
        print('bezet', q)
        vikingleden=Vikinglid.objects.all()
    print('context', vikingleden.count())
    print('billable', billable.count())
    context = {
        'vikingleden':vikingleden,
        'topics': topics, 
        'topcs':topcs,
        'empty':leeg,
        'billable':billable,
        'legen':leeg.count(),
        'q':q,
        }
    return render(request, template, context)
    

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

# @login_required(login_url='login')
def createVikinglid(request):
    form = VikinglidForm()
    topics = Activiteit.objects.all()
    try:
        vikinglid = Vikinglid.objects.get(name='Wachtlijst')
        messages.error(request, 'VIKINGLID  try tijdelijk ', vikinglid)
        print('vikinglid==>' ,vikinglid)
    except:
        vikinglid = Vikinglid.objects.all().last()
        messages.error(request, 'VIKINGLID except tijdelijk ',vikinglid)
    if request.method == 'POST':
        username = request.POST.get('name').lower()
        if username:
            email='info@mantisbv.nl-unknown'
            try:
                vikinglid=Vikinglid.objects.all().get(name=username)
            except:
                print('vikinglid not found', username)
                vikinglid=Vikinglid.objects.create(
                    email=email,
                    avatar='avatar.svg',
                    name=username,
                )
                try:
                    email='info@mantisbv.nl-unknown'
                    user = User.objects.get(username = username)
                except:
                    print('user not found', username)
                    email = request.POST.get('email')
                    topic_name = request.POST.get('islidvan')
                    username = request.POST.get('name').lower()
                    password ='pbkdf2_sha256$390000$YrBnItyjcuUgxrlMGlWFPH$HBlBExsE2C5EcmEmhHvtDTkMl3PH+0E7EQJLrWER4cs=' 
                    # 'viking123'
                    try:
                        user = User.objects.get(username = username)
                    except:
                        user = authenticate(request, username=username, password=password)
                        user=User.objects.create(
                        email = email,
                        is_active=True,
                        username = username,
                        password=password,
                        )
                    else:
                        messages.error(request, 'VIKINGLID  already exists ')
        return redirect('home')
    vikinglid=Vikinglid.objects.all().last()
    leeg = Activiteit.objects.all().filter(
        # Q(lid_van=None) &
        # Q(type='kluis') |
        Q(name='Wachtlijst')
        )
    context = {
        'form': form,
          'topics': topics,
          'kluizen': leeg,
          'vikinglid':vikinglid}
    return render(request, 'viking/vikinglid_form.html', context)

def aanvrage(request):
    form = VikinglidForm()
    topics = Activiteit.objects.all()
    # try:
    #     vikinglid = Vikinglid.objects.get(name='Wachtlijst')
    #     messages.error(request, 'VIKINGLID  try tijdelijk ', vikinglid)
    #     print('vikinglid==>' ,vikinglid)
    # except:
    #     vikinglid = Vikinglid.objects.all().last()
    #     messages.error(request, 'VIKINGLID except tijdelijk ',vikinglid)
    if request.method == 'POST':
        username = request.POST.get('name').lower()
        description = request.POST.get('description') #.lower()
        if username:
            email='info@mantisbv.nl-unknown'
            try:
                vikinglid=Vikinglid.objects.all().get(name=username)
            except:
                print('vikinglid not found', username)
                vikinglid=Vikinglid.objects.create(
                    email=email,
                    avatar='avatar.svg',
                    name=username,
                    description=description
                )
        return redirect('home')
    vikinglid=Vikinglid.objects.all().last()
    leeg = Activiteit.objects.all().filter(
        # Q(lid_van=None) &
        # Q(type='kluis') |
        Q(name='Wachtlijst')
        )
    context = {
        'form': form,
          'topics': topics,
          'kluizen': leeg,
          'vikinglid':vikinglid}
    return render(request, 'viking/aanvrage_form.html', context)


@login_required(login_url='login')
def urv_updateKluis(request, pk):
    vikinglid=Vikinglid.objects.get(id=pk)
    form=VikinglidForm(instance=vikinglid)
    kluizen=Activiteit.objects.all().filter(type='kluis').order_by('name')
    teams=Activiteit.objects.all().filter(type='ploeg').order_by('name')
    lidvan = vikinglid.is_lid_van.all()
    kluisje= request.POST.getlist('heeftkluis')
    kluisjeopheffen= request.POST.getlist('is_lid_van')
    if kluisje:
        try:
            vikinglid.is_lid_van.add(kluisje[0])
        except:
            print('activiteit',kluisje[0])
            pass
    if kluisjeopheffen:
        try:
            vikinglid.is_lid_van.remove(kluisjeopheffen[0])
        except:
            print('op te heffen',kluisjeopheffen[0])
            pass


    if request.method == 'POST':
        vikinglid.name = vikinglid.name
        vikinglid.name = request.POST.get('name')
        vikinglid.email = request.POST.get('email')
        vikinglid.save()
        return redirect('home')

    context = {
        'form': form,
          'vikinglid': vikinglid,
          'lidvan':lidvan,
          'kluizen':kluizen,
          'teams':teams,
    }
    return render(request, 'viking/vikinglid_form.html', context)

@login_required(login_url='login')
def deleteVikinglid(request, pk):

    vikinglid = Vikinglid.objects.get(id=pk)
    if request.method == 'POST':
        vikinglid.delete()
        return redirect('home')

    context = {'obj': vikinglid}
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
    # topics = Activiteit.objects.filter(name__icontains=q)
    topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'viking/topics.html', {'topics': topics})


def activityPage(request):
    # room_messages = Message.objects.all()
    activiteit = Activiteit.objects.all()[0:10]
    return render(request, 'viking/activity.html', {'activiteiten': activiteit})


def KluisPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    kluisjes=Kluis.objects.all().filter(name__contains=q) #.exclude(participants=None)
    return render(request, 'viking/kluis_list.html', {'kluisjes': kluisjes})

@api_view(['GET'])
def gebruikerslijst(request):
    gebruikers=User.objects.all()
    serializer=GebruikerSerializer(gebruikers,many=True)

    return Response(serializer.data)

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


@login_required(login_url='login')
def kluisje(request, kluis_id):
    kluis = get_object_or_404(Activiteit, pk=kluis_id)
    form = KluisjeForm(instance=kluis)
    kluisjes=Activiteit.objects.all()
    toegewezen=Vikinglid.objects.all().exclude(is_lid_van__id=None)
    billable=kluis.lid_van.all()
    leden=Vikinglid.objects.all().filter(is_lid_van__id=None)
    print('billable', billable)
    if request.method == 'POST':
        # kluis.topic = request.POST.get('topic')
        kluis.topic = 'kluis' 
        kluis.name = request.POST.get('name')
        for af in request.POST.getlist('org_list'):
            try:
                v=Vikinglid.objects.get(pk=af)
                kluis.lid_van.add(v)
                print('kluis.id, af', kluis.id,af,v)
            except:pass
        kluis.save()
        return redirect('home')
    return render(request, 'viking/kluisje_form.html', {
            'kluis': kluis,
            'form': form,
            'leden': leden,
            'kluisjes': kluisjes,
            'toegewezen': toegewezen,
            'billable': billable,
            'error_message': "Er is geen keuze gemaakt.",
        })
    return HttpResponseRedirect(reverse('kluisje', args=(kluis_id,)))

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
    return render(request, 'viking/vikinglid-detail.html', {
            'vikinglid': vikinglid,
            'users': personen,
            # 'roeiers': roeiers,
            'kandidaten':kandidaten,
            'islidvan':islidvan, 
            'error_message': "Er is geen keuze gemaakt.",
        })

# class AanmeldView(ListView):
#     template_name='viking/aanmeldview.html'
#     def get_context_data(self, **kwargs):
#         x=0
#         year=int(date.today().strftime('%Y'))
#         month = int(date.today().strftime('%m'))
#         volgendemaand=month
#         monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
#         x+=1
#         if month <= 12 and x==0: volgendemaand=month+1
#         einde=monthend[volgendemaand]
#         end=date(year,month,einde)
#         beginmonth = 1 #int(date.today().strftime('%m'))
#         endmonth = 12 # int(date.today().strftime('%m'))
#         monthend=[0,31,28,31,30,31,30,31,31,30,31,30,31] #jfmamjjasond
#         einde=monthend[endmonth]
#         # aantalregels=10
#         start=date(year,beginmonth,1)
#         end=date(year,endmonth,einde)
#         start=date(year,beginmonth,1)
#         # rooster=Flexevent.objects.filter(datum__range=[start, end])
#         # roostergedeeltelijk=Flexevent.objects.filter(datum__range=[start, end])
#         context = {
#         # 'rooster': rooster,
#         } 
#         return context


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

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

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

# @api_view(['GET'])
# def getRoutes(request):

#     routes = [
#         {
#             'Endpoint': '/notes/',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns an array of notes'
#         },
#         {
#             'Endpoint': '/notes/id',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns a single note object'
#         },
#         {
#             'Endpoint': '/notes/create/',
#             'method': 'POST',
#             'body': {'body': ""},
#             'description': 'Creates new note with data sent in post request'
#         },
#         {
#             'Endpoint': '/notes/id/update/',
#             'method': 'PUT',
#             'body': {'body': ""},
#             'description': 'Creates an existing note with data sent in post request'
#         },
#         {
#             'Endpoint': '/notes/id/delete/',
#             'method': 'DELETE',
#             'body': None,
#             'description': 'Deletes and exiting note'
#         },
#     ]
#     return Response(routes)

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

@api_view(['GET', 'POST'])
def getActiviteiten(request):
    aktiviteiten = Activiteit.objects.all() #.order_by('-updated')
    leeg = Activiteit.objects.all().filter(
        Q(lid_van=None) &
        Q(type='kluis')|
        Q(name='Wachtlijst')
        )
    
    serializer = ActiviteitSerializer(leeg, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getActiviteit(request,pk):
    aktiviteit = Activiteit.objects.get(id=pk)
    serializer = ActiviteitSerializer(aktiviteit, many=False)
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
