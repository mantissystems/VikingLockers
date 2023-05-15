from django.core.mail import send_mail
from django.template import loader
import csv
from django.http import HttpResponse
import io
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
from collections import namedtuple
from django.db import connection
from django.views.generic import(ListView,UpdateView,DetailView,TemplateView)
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
    TopicSerializer,
)
from .models import   Topic,Vikinglid,Note,Matriks,KluisjesRV ,Kluislabel,Instromer
from base.models import Message
# from .forms import UserForm,VikinglidForm,KluisjeForm ,InstromerForm

# def loginPage(request):

#     page = 'login'

#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username').lower()
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username = username)
#         except:
#             messages.error(request, 'User does not exist')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'User name or password does not exist')

#     context = {'page': page}
#     return render(request, 'viking/login_register.html', context)

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
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    template='viking/home.html'
    topics = Topic.objects.all()
    from django.db.models import Count
    result = (KluisjesRV.objects
    .values('topic')
    .annotate(dcount=Count('topic'))
    .order_by()
)
    all=Vikinglid.objects.all()
    filter1=Q(name__icontains=q)    
    vikingleden=Vikinglid.objects.all().filter(filter1)[0:10]
    gevonden=KluisjesRV.objects.none
    aanvragen=Message.objects.all()
# ==========================================================
    fkluis=Q(kluisnummer__icontains=q)    
    fnaam=Q(naamvoluit__icontains=q)    
    fhuurdersnaam=Q(huurders__name__icontains=q)    
    ftopic=Q(topic__icontains=q)    
    kasten=KluisjesRV.objects.all().order_by('kluisnummer').filter((fkluis|fnaam))
    kluizen=KluisjesRV.objects.all().order_by('kluisnummer').filter((fkluis|fnaam|fhuurdersnaam|ftopic))
    if q!='':gevonden=KluisjesRV.objects.all().order_by('kluisnummer').filter((fkluis|fnaam|fhuurdersnaam|ftopic))
    bezet=KluisjesRV.objects.all().order_by('kluisnummer').exclude(huurders=None)
    gevondeninmatriks=KluisjesRV.objects.all().order_by('kluisnummer').filter((fhuurdersnaam|fnaam)).values_list('kluisnummer')
    hit=Matriks.objects.filter(regel__icontains=gevondeninmatriks)
# ==============================================================
    filterregel=Q(regel__icontains=q)    
    filterregel2=Q(naam__icontains=q)    
    heren=Matriks.objects.all().filter(naam__icontains='Heren').filter(filterregel|filterregel2).exclude(y_as__in=(7,8)).order_by('y_as')
    adames=Matriks.objects.all().filter(naam__startswith='A').filter(filterregel|filterregel2).exclude(y_as__in=(7,8)).order_by('y_as')
    bdames=Matriks.objects.all().filter(naam__startswith='B').filter(filterregel|filterregel2).exclude(y_as__in=(7,8)).order_by('y_as')
    cdames=Matriks.objects.all().filter(naam__startswith='C').filter(filterregel|filterregel2).exclude(y_as__in=(7,8)).order_by('y_as')
    ddames=Matriks.objects.all().filter(naam__startswith='D').filter(filterregel|filterregel2).exclude(y_as__in=(7,8)).order_by('y_as')
    mtrx=Matriks.objects.all().filter(filterregel).exclude(y_as__in=(7,8))
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    wachtlijst=KluisjesRV.objects.get(naamvoluit='wachtlijst')
    body=request.POST.get('body')
    print(body)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=wachtlijst,
            body=request.POST.get('body')
        )
    for i in range (0,13):
        kopmtrx.append(hdr[i])
    context = {
        'koplegen':[f'verdeling ({all.count()} leden'],
        'vikingleden':vikingleden,
        'topics': result, 
        'matrix': mtrx,
        'heren': heren,
        'adames': adames,
        'bdames': bdames,
        'cdames': cdames,
        'ddames': ddames,
        'kluizen': kluizen,
        'bezet': bezet,
        'kopmtrx': kopmtrx,
        'kasten': kasten,
        'hit': hit,
        'aanvragen': aanvragen,
        'q':q,
        'gevonden':gevonden,
        }
    return render(request, template, context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    wachtlijst=KluisjesRV.objects.get(naamvoluit='wachtlijst')
    body=request.POST.get('body')
    print(body)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=wachtlijst,
            body=request.POST.get('body')
        )

    context = {
        'user': user, 
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
    topics = Topic.objects.all()
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
    context = {
        'form': form,
          'topics': topics,
          'vikinglid':vikinglid}
    return render(request, 'viking/vikinglid_form.html', context)

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'viking/aarjoesjoer.html', {'obj': message})

def mutatie(request):
    form = InstromerForm()
    topics = Topic.objects.all()
    description='aanvraag..'
    context = {
            'form': form,
            'topics': topics,
            }
# if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = InstromerForm(request.POST)
        # check whether it's valid:
        your_name= request.POST.get('your_name')
        print('vikinglid', your_name,description)
        lid, created = Instromer.objects.create(
                name=your_name,
                )
        if form.is_valid():
            print('form is valid')
            username = form.cleaned_data["your_name"]
            print('vikinglid', username,description)
            # email = form.cleaned_data["email"]
            # description = form.cleaned_data["description"]
            lid, created = Instromer.objects.create(
                name=username,
                # email=email,
                #     avatar='avatar.svg',
                # description=description,
                )

    #     message = form.cleaned_data["message"]
    #     sender = form.cleaned_data["sender"]
    #     cc_myself = form.cleaned_data["cc_myself"]

    # recipients = ["info@example.com"]
    # if cc_myself:
    #     recipients.append(sender)

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = NameForm()

    return render(request, "viking/instromer_form.html", {"form": form})
   

def export_team_data(request):
    # https://docs.djangoproject.com/en/3.2/howto/outputting-csv/
    # toetsenbord testen
    # response = HttpResponse(
    #     content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="ploegen_lijst.csv"'},
    # )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="kluislijst.csv"'

    writer = csv.writer(response)

    csv_data = KluisjesRV.objects.all().values_list(
        'name', 'location')
    t = loader.get_template('viking/export_teamlid_data.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response

def kluis(request, pk):
    vikingers=Vikinglid.objects.all().order_by('name')
    try:
        kls=KluisjesRV.objects.get(id=pk)
        form=KluisjeForm(instance=kls)
        huurders=kls.huurders.all()
        context={
                'huurders':huurders,
                'form': form,
                'kluis': kls,
                'vikingers':vikingers,
            }
    except:
        pass
    if request.method == 'POST':
            huurder= request.POST.get('heeftkluis')
            your_name= request.POST.get('your_name')
            opheffen= request.POST.get('opheffen')
            if kls:
                    if huurder or your_name:
                        kls.naamvoluit=huurder
                        kluisnummer=kls.kluisnummer
                        setattr(kls, 'kluisnummer',kluisnummer)
                        kls.save()
                    if opheffen:
                        setattr(kls, 'kluisnummer', '---')
                        kls.save()
                        
            return redirect('home')

    return render(request, 'viking/update_kluis_form.html', context)

def decodeer(regel,de_matriks_kolom,column,cellengte):
    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer

@login_required(login_url='login')
def update_kluis(request, pk,kol):
    column=int(kol)
    matrix=Matriks.objects.get(id=pk)
    labels=Kluislabel.objects.all()
    rms = KluisjesRV.objects.all() #.exclude(huurders=None)
    owner_count=0
    rgl=matrix.y_as
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    vikingers=Vikinglid.objects.all().order_by('name')
    dematrikskolom=hdr[column];print(dematrikskolom)
    kluisje=getattr(matrix,dematrikskolom)
    matriksnaam=getattr(matrix,'naam')
    context={}
    opheffen= request.POST.get('opheffen')
    cellengte=4
    column=int(kol)
    regel=matrix.regel
    de_matriks_kolom=hdr[column]

    try:
        oorspronkelijkmatriksnummer=decodeer(regel,de_matriks_kolom,column,cellengte)
        kls=KluisjesRV.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
        form=KluisjeForm(instance=kls)
        context = {
                'form': form,
                'kluis': kls,
                'vikingers':vikingers,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
    except:
        kluisfilter1=Q(row=rgl)
        kluisfilter2=Q(col=column)
        kluisfilter3=Q(topic=matriksnaam)
        kls=KluisjesRV.objects.filter((kluisfilter1&kluisfilter1)|kluisfilter3).first()
        print('except: ',matriksnaam, 'rij',rgl,'kolom',column,kls)
    finally:
        vikingers=Vikinglid.objects.all().order_by('name')

        context = {
                'vikingers':vikingers,
                'kluis': kls,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
        if kls:
            huurders=kls.huurders.all()
            context={
                'huurders':huurders,
                'vikingers':vikingers,
                'labels': labels,
                'kluis': kls,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
}

        if request.method == 'POST':
            huurder= request.POST.get('heeftkluis')
            label= request.POST.get('kluislabel')
            slot= request.POST.get('slot')
            your_name= request.POST.get('your_name')
            huuropheffen= request.POST.get('huuropheffen')
            if kls:
                    if slot:
                        kls.type=slot
                        kls.save()
                    if label:
                        kls.label=label
                        mx=Matriks.objects.all().filter(regel__icontains=oorspronkelijkmatriksnummer).first()
                        setattr(mx,hdr[int(kls.col)],label)
                        mx.save()
                        kls.save()
                    if huurder or your_name:
                        h=Vikinglid.objects.get(id=huurder)
                        kls.huurders.add(h)
                        setattr(kls, 'verhuurd',True)
                        kls.save()
                    if huuropheffen:
                        h=Vikinglid.objects.get(id=huuropheffen)
                        print('opheffen',h)
                        kls.huurders.remove(h)
                        setattr(kls, 'verhuurd',False)
                        kls.save()
                        
            return redirect('home')
    return render(request, 'viking/update_kluis_form.html', context)

class KluisList(ListView):
    queryset=KluisjesRV.objects.all()

class Blokken(TemplateView):
    template_name = 'viking/home.html'
    def get_context_data(self, **kwargs):
        kasten=['Heren','Adames','Bdames','Cdames','Ddames']
        Matriks.objects.all().delete()
        hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']
        for k in kasten:
            regelteller=0
            print(k)
            matrixnaam=k 
            bloknummer='' ;   vv=matrixnaam[0:1]      #voorvoegsel
            nr=8
            kolommen = nr
            rounds=nr
            r = 0
            rijen=nr
            s = ""
            w1=''
            p = 0
            for teama in range(0,kolommen): 
                s = ""
                p = 0
                for teamb in range(0,kolommen):
                    if teama != teamb:
                        p += 1
                        ronde = (teamb + teama)%kolommen
                        if ronde == 0: ronde = kolommen
                        r+=1
                        s += vv + str(r).zfill(3) #+'|.'
                        if p%2 == 0:
                            w1 += str(ronde)
                            w1 = ""
                        else:
                            r+=1
                            s += vv + str(r).zfill(3) #+'|!'
                            ronde += 1

                    if teama == teamb:
                        r+=1
                        s +=vv +  str(r).zfill(3) #+'|='

                print(s)
                # ALS DE MATRIKS AL IS AANGEMAAKT,NIET MEER UITVOEREN, wordt opgenomen in het instellingen bestand
                regelteller+=1
                Matriks.objects.update_or_create( 
                        kop=s,
                        regel=s,ronde=r,x_as=r,y_as=regelteller,naam=matrixnaam,)            
        koppel_kluis_met_matriks(request)
        return

# @login_required(login_url='login')
def koppel_kluis_met_matriks(request):
    print('in koppel_kluis_met_matriks')
    matrix=Matriks.objects.all()
    hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13',]
    teller=0
    tel= KluisjesRV.objects.all().order_by('id').first()
    mx= KluisjesRV.objects.all().order_by('id').last()
    max=mx.id
    teller=tel.id
    for m in matrix:
        for k in hdr:
            inh=getattr(m,k)
            kastje=getattr(m,k)
            try:
                vl=KluisjesRV.objects.get(kluisnummer=inh)
                setattr(vl, 'kluisje',inh)
                vl.save()
            except:
                pass
            if teller<max: teller+=1
    print('einde koppelen ===============')
    return

@login_required(login_url='login')
def hernummermatriks(request):
    print('in hernummermatriks===============')
    # rij=0
    # matriks regel-kolomnummering naar kolomvelden overbrengen
    hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12',]#'kol13',] #'kol14']
    begincell=0;cellengte=0;eindcell=0
    matrix=Matriks.objects.all().order_by('naam','y_as')
    kolomteller=0
    for m in matrix:
        rij=str(m.y_as)
        cellengte=4
        regel=m.regel
        for h in hdr:
            de_matriks_kolom=h
            inh=getattr(m,h)
            if m.x_as/m.y_as==kolomteller:
                kolomteller=0
            kolomteller+=1
            oorspronkelijkmatriksnummer=decodeer(regel,de_matriks_kolom,kolomteller,cellengte)            
            try:
                vl=KluisjesRV.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
                if vl.huurders.all().count()==0:
                    print(m.naam,de_matriks_kolom,inh,h)
                    vl.save()
            except:
                # will be part of settings
                # c='---'   #set the mismatch string  
                inh=getattr(m,h)                                            #ON
                # print('mismatch',inh,de_matriks_kolom,oorspronkelijkmatriksnummer) #ON
                c='r'+ rij + 'k' +de_matriks_kolom[3:]                   #ON
            #     # c=vl.row + vl.col
                setattr(m, de_matriks_kolom, c)  #puts a hit in the cell or a mismatch '---'   #ON
            #     # setattr(m, de_matriks_kolom, 'rij'+ rij.zfill(2) + de_matriks_kolom)          #OFF
                m.save()

                # pass
            setattr(m, de_matriks_kolom, oorspronkelijkmatriksnummer)
            # vl.kluisje='rij'+ rij.zfill(2) + de_matriks_kolom #off when handout is true       #OFF
            # vl.row=rij.zfill(2)
            # vl.col=de_matriks_kolom[3:].zfill(2)
            # print('match',vl.col) #ON
            # setattr(m, de_matriks_kolom, 'rij'+ rij.zfill(2) + de_matriks_kolom)              #OFF
            # vl.save()
            m.save()

    print('einde hernummermatriks===============')
    koppel_kluis_met_matriks(request)
    context={}
    return render(request, 'viking/home.html', context)
def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False
@login_required(login_url='login')
def check_matriks(request):
    print('in check_matriks')
    print('check kastje met kluisnummer; en huurder toevoegen')
    hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13',]
    krv= KluisjesRV.objects.all()
    try:
        wachtlijst=KluisjesRV.objects.get(naamvoluit='wachtlijst')
    except:
        wl=KluisjesRV.objects.update_or_create(naamvoluit='wachtlijst')
    l=0
    for rv in krv:
        if 'Heren' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[6:l]):
                rv.kluisnummer='H' + rv.kastje[6:l].zfill(3)
                rv.label='H_' + rv.kastje[6:l].zfill(2) #H_01
                rv.topic=rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
        if 'Dames' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[5:l]):
                rv.kluisnummer='D' + rv.kastje[6:l].zfill(3)
                rv.label='D_' + rv.kastje[6:l].zfill(2)
                rv.topic='D' +rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
        if 'Dames A' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[8:l]):
                rv.kluisnummer='A' + rv.kastje[8:l].zfill(3)
                rv.label='A_' + rv.kastje[6:l].zfill(2)
                rv.topic='A' +rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
        if 'Dames B' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[8:l]):
                rv.kluisnummer='B' + rv.kastje[8:l].zfill(3)
                rv.label='B_' + rv.kastje[6:l].zfill(2)
                rv.topic='B' +rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
        if 'Dames C' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[8:l]):
                rv.kluisnummer='C' + rv.kastje[8:l].zfill(3)
                rv.label='C_' + rv.kastje[6:l].zfill(2)
                rv.topic='C' +rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
        print(rv.kluisnummer,rv.label,rv.col,rv.row)
        m=Matriks.objects.filter(regel__icontains=rv.kluisnummer).first()
        if m:
            m.regel=m.kop
            if isNum(rv.col):
                c=        int(rv.col)
                setattr(m,hdr[c],rv.label)
                m.save()
    context={}
    # return
    return render(request, 'viking/home.html', context)

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

@api_view(['GET', 'POST'])
def getTopics(request):
    notes = Topic.objects.all()
    serializer = TopicSerializer(notes, many=True)
    return Response(serializer.data)


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


@login_required(login_url='login')
def get_kluis(request, pk,kol):
    context={}
    return render(request, 'viking/get_kluis_form.html', context)

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
    topics = Topic.objects.filter(name__icontains=q)
    from django.db.models import Count
    result = (KluisjesRV.objects
    .values('topic')
    .annotate(dcount=Count('topic'))
    .order_by()
)

    return render(request, 'viking/topics.html', {'topics': result})

@login_required(login_url='login')
def verhuurPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    fkluis=Q(kluisnummer__icontains=q)    
    fnaam=Q(naamvoluit__icontains=q)    
    ftopic=Q(topic__icontains=q)    
    kluizen=KluisjesRV.objects.all().order_by('kluisnummer').filter((fkluis|fnaam|ftopic))
    context = {
        'kluizen': kluizen,
        'q':q,
        }

    return render(request, 'viking/activiteiten.html', context)

def file_load_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="matriks_as_is.csv"'},
    )
    header= 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol12','kol13'
    header={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    csv_data=Matriks.objects.all().exclude(y_as__in=(7,8)).order_by('naam')
    # csv_data=header|csv_data
    t = loader.get_template('viking/export_matriks.txt')
    c = {'data': csv_data,'hdr':header}
    response.write(t.render(c))
    return response

#  =========== EXPORT TEST RUBBUSH HEREAFTER ========================

# def some_view(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(
#     content_type='text/csv',
#     headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
#     )

#     # The data is hard-coded here, but you could load it from a database or
#     # some other source.
#     csv_data = (
#         ('First row', 'Foo', 'Bar', 'Baz'),
#         ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
#     )

#     t = loader.get_template('viking/my_template_name.txt')
#     c = {'data': csv_data}
#     response.write(t.render(c))
#     return response

# class Echo:
#     """An object that implements just the write method of the file-like
#     interface.
#     """
#     def write(self, value):
#         """Write the value by returning it, instead of storing in a buffer."""
#         return value

# def some_view(request):
#     # import reportlab
#     # from django.http import FileResponse
#     # from reportlab.pdfgen import canvas

#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer)

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     # See the ReportLab documentation for the full list of functionality.
#     p.drawString(10, 10, "Hello world.")

#     # Close the PDF object cleanly, and we're done.
#     p.showPage()
#     p.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename='hello.pdf')