from django.core.mail import send_mail
from django.template import loader
import csv
from django.http import HttpResponse
# from django.http import StreamingHttpResponse
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
    ActiviteitSerializer,
    TopicSerializer,
)
from .models import   Topic,Vikinglid,Activiteit,Note,Matriks,KluisjesRV 
from .forms import UserForm,Urv_KluisForm,VikinglidForm,KluisjeForm

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
# ==========================================================
    kopmtrx="[f'kast', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']," #'regel-informatie kluisnummers'
    filter2=Q(kluisnummer__icontains=q)    
    filter3=Q(naamvoluit__icontains=q)    
    filter4=Q(huurders__name__icontains=q)    
    filter5=Q(topic__icontains=q)    
    # wb=KluisjesRV.objects.all().order_by('kluisnummer').filter(huurders__name__contains='van')
    # print(wb)
    if q=='Export Kluislijst':
            return redirect('export')
    if q=='Aanvraag':
            return redirect('create-aanvrage')
    kasten=KluisjesRV.objects.all().order_by('kluisnummer').filter((filter2|filter3))
    # kluizen=KluisjesRV.objects.all().order_by('kluisnummer').exclude(filter4)
    kluizen=KluisjesRV.objects.all().order_by('kluisnummer').filter((filter2|filter3|filter4|filter5))
    bezet=KluisjesRV.objects.all().order_by('kluisnummer').exclude(huurders=None)
# ==============================================================
    filterregel=Q(regel__icontains=q)    
    filterregel2=Q(naam__icontains=q)    
    heren=Matriks.objects.all().filter(naam__icontains='heren').filter(filterregel|filterregel2)
    adames=Matriks.objects.all().filter(naam__startswith='A').filter(filterregel|filterregel2)
    bdames=Matriks.objects.all().filter(naam__startswith='B').filter(filterregel|filterregel2)
    cdames=Matriks.objects.all().filter(naam__startswith='C').filter(filterregel|filterregel2)
    ddames=Matriks.objects.all().filter(naam__startswith='D').filter(filterregel|filterregel2)
    mtrx=Matriks.objects.all().filter(filterregel)
    context = {
        'koplegen':[f'verdeling ({all.count()} leden'],
        'vikingleden':vikingleden,
        'topics': result, 
        'matrix': mtrx,
        # 'kopmtrx' : [f'kast', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13'], #'regel-informatie kluisnummers'
        'heren': heren,
        'adames': adames,
        'bdames': bdames,
        'cdames': cdames,
        'ddames': ddames,
        'kluizen': kluizen,
        'bezet': bezet,
        'kasten': kasten,
        'q':q,
        }
    return render(request, template, context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    # rooms = user.room_set.all()
    # room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    context = {
        'user': user, 
        # 'rooms': rooms, 
        # 'room_messages': room_messages,
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
        Q(name='Wachtlijst')
        )
    context = {
        'form': form,
          'topics': topics,
          'kluizen': leeg,
          'vikinglid':vikinglid}
    return render(request, 'viking/aanvrage_form.html', context)

def export_team_data(request):
    # https://docs.djangoproject.com/en/3.2/howto/outputting-csv/
    # toetsenbord testen
    # response = HttpResponse(
    #     content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="ploegen_lijst.csv"'},
    # )
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="kluislijst.csv"'

    writer = csv.writer(response)

    csv_data = Kluis.objects.all().values_list(
        'name', 'location')
    t = loader.get_template('viking/export_teamlid_data.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response

def kluis(request, pk):
    vikingers=Vikinglid.objects.all().order_by('name')
    # dematrikskolom=hdr[column];print(dematrikskolom)
    # kluisje=getattr(matrix,dematrikskolom)
    # matriksnaam=getattr(matrix,'naam')
    # match='rij'+str(rgl)+'kol'+kol
    # context={}
    try:
        kls=KluisjesRV.objects.get(id=pk)
        form=KluisjeForm(instance=kls)
        context = {
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
                        # print(huurder,matrix.y_as,kls.kluisnummer,)
                        # setattr(matrix, dematrikskolom, kluisnummer)
                        # matrix.save()
                        setattr(kls, 'kluisnummer',kluisnummer)
                        kls.save()
                    if opheffen:
                        # setattr(matrix, dematrikskolom, '---')
                        # matrix.save()
                        setattr(kls, 'kluisnummer', '---')
                        kls.save()
                        
            return redirect('home')

    return render(request, 'viking/update_kluis_form.html', context)

def decodeer(regel,de_matriks_kolom,column,cellengte):
    # regel=matrix.regel
    # de_matriks_kolom=hdr[column]
    # regellengte=len(regel)

    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    # print(b)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer

def update_kluis(request, pk,kol):
    column=int(kol)
    print('in update_kluis')
    matrix=Matriks.objects.get(id=pk)
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
        print('oorspronkelijkmatriksnummera',oorspronkelijkmatriksnummer)
        kls=KluisjesRV.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
        # huurders=kls.huurders.all()
        form=KluisjeForm(instance=kls)
        print('try:',kluisje,kls.id,oorspronkelijkmatriksnummer)
        context = {
                'form': form,
                'kluis': kls,
                'vikingers':vikingers,
                # 'huurders': huurders,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
    except:
        kluisfilter1=Q(row=rgl)
        kluisfilter2=Q(col=column)
        kluisfilter3=Q(topic=matriksnaam)
        kls=KluisjesRV.objects.filter((kluisfilter1&kluisfilter1)|kluisfilter3).first()
        print('except: ',matriksnaam, 'rij',rgl,'kolom',column,kls)
    finally:
        # kluisfilter1=Q(row=rgl)
        # kluisfilter2=Q(col=column)
        # kluisfilter3=Q(topic=matriksnaam)
        # kls=KluisjesRV.objects.filter((kluisfilter1&kluisfilter1)|kluisfilter3).first()
        # print('except: ',matriksnaam, 'rij',rgl,'kolom',column,kls)
        vikingers=Vikinglid.objects.all().order_by('name')

        context = {
                # 'huurders': huurders,
                'vikingers':vikingers,
                'kluis': kls,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
        if kls:
            huurders=kls.huurders.all()
            context={
                'huurders':huurders,
                'vikingers':vikingers,
                'kluis': kls,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
}

        if request.method == 'POST':
            huurder= request.POST.get('heeftkluis')
            your_name= request.POST.get('your_name')
            huuropheffen= request.POST.get('huuropheffen')
            if kls:
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

class Blokken(TemplateView):
    template_name = 'viking/home.html'
    def get_context_data(self, **kwargs):
        kasten=['Heren','Adames','Bdames','Cdames','Ddames']
        Matriks.objects.all().delete()
        hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9'] #,'kol10','kol11','kol12','kol13']
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

def get_matrix(request):
    template_name = 'viking/bloktabel_list.html'
    nr=9
    kolommen = nr
    kasten=Kluis.objects.all() #.filter(kast__icontains=bloknummer)
    mtrx=Matriks.objects.all()
    topics=Topic.objects.all()
    heren=Matriks.objects.all().filter(naam__icontains='heren')
    dames=Matriks.objects.all().filter(naam__icontains='dames')
    rounds=nr #int(kolommen/2)
    # r = 0
    rijen=nr # (kolommen-1)*rounds
    spelers=Vikinglid.objects.all() #.filter(nr=str(t).zfill(2)).values_list('naam')
    context={'kop': [f'matrix ({rijen}rijen) bij {kolommen} kolommen',],
            'kopmtrx' : [f'kast', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13'], #'regel-informatie kluisnummers'
            # 'regels': Matriks.objects.all(),
            'matrix': mtrx,
            'heren': heren,
            'dames': dames,
            'topics': topics,
             'kopspelers': [f'matrix({rijen}rijen; {rounds} rijen) with {kolommen} kolommen'],
            # 'spelers': spelers,

            }
    return render(request,"viking/bloktabel_list.html", context)

@login_required(login_url='login')
def set_kluis(request, pk,kol):
    # kls=Kluis.objects.get(id=kol)
    vikingers=Vikinglid.objects.all().order_by('name')
    matrix=Matriks.objects.get(id=pk)
    hdr=[ 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10']#,'kol10','kol11','kol12','kol13']
    a=hdr[int(kol)]
    col=int(kol)
    k=getattr(matrix,a)
    # print(k)
    # het idee is om de getoonde informatie in de regel op te slaan en de getoonde informatie in kol te vervangen op de positie van de cel in de regel.
    # dus als getoond wordt '1', dan staat op pos 1 '001'. de regel ontvangt het kluis-id. de kol ontvangt '001'; de kluis is BEZET
    # de kol's bevatten het kluisnummer. x-as is id, y-as =kol;
    
    pos=int(kol);begincell=0;cellengte=0;eindcell=0
    cellengte=3
    regellengte=len(matrix.regel)
    begincell=col+pos*cellengte
    eindcell=0+cellengte
    regel=matrix.regel
    cell=regel[begincell:eindcell]
    rechts=regel[eindcell+cellengte:regellengte]
    new_cell_content=' xxx' ; huurder='';huurdernaam=''
    if col in (1,2,3,4,5,6,7,8,9,10,11,12,13):
        b=(col-1)*cellengte
        e=b+3
        c=regel[b:e] 
        new_info=c
        new_cell_content=c 
        print('karakters per regel',regellengte,'column', col,'celinhoud',c)
        try:            
            kls=Kluis.objects.get(id=c)
        except:
            pass
        finally:
            kls=Kluis.objects.get(id=c)
            form=KluisjeForm(instance=kls)
            # form=VikinglidForm(instance=kls)

    if col==1: matrix.kol1=new_cell_content
    if col==2: matrix.kol2=new_cell_content
    if col==3: matrix.kol3=new_cell_content
    if col==4: matrix.kol4=new_cell_content
    if col==5: matrix.kol5=new_cell_content
    if col==6: matrix.kol6=new_cell_content
    if col==7: matrix.kol7=new_cell_content
    if col==8: matrix.kol8=new_cell_content
    if col==9: matrix.kol9=new_cell_content
    if col==10: matrix.kol10=new_cell_content
    if col==11: matrix.kol11=new_cell_content
    if col==12: matrix.kol12=new_cell_content
    if col==13: matrix.kol13=new_cell_content
    # form=KluisjeForm(instance=kls)
    kluizen=Activiteit.objects.all().filter(type='kluis').order_by('name')
    teams=Activiteit.objects.all().filter(type='ploeg').order_by('name')
    kluisje= request.POST.getlist('heeftkluis')
    kluisjeopheffen= request.POST.getlist('is_lid_van')
    if request.method == 'POST':
        h = request.POST.getlist('huurder')
        print('huurder',h[0])
        h=h[0]
        huurder=int(h)
        hrdr=Vikinglid.objects.get(id=huurder)
        kls.name = kls.name
        kls.name =hrdr.name # request.POST.get('name')
        kls.email = request.POST.get('email')
        kls.save()
        return redirect('get_matrix')

    context = {
        'form': form,
          'vikinglid': kls,
          'vikingers':vikingers,
          'kluizen':kluizen,
          'teams':teams,
    }
    return render(request, 'viking/get_kluis_form.html', context)

# @login_required(login_url='login')
def koppel_kluis_met_matriks(request):
    print('in koppel_kluis_met_matriks')
    matrix=Matriks.objects.all()
    # kluis=Kluis.objects.all().update(code='')
    # doorloop alle velden
    # 1.koppel van iedere regel en iedere kolom de eerstvolgende kluis <-----=== 
    #   -dus per regel een loop door kluis
    #   - in de loop; zet in kluis.kast hetcelnummer: bijv 'h001' 
    # 2.SUSPEND: controleer: dame in dames; heer in heren
    # mismatch dames; kluis.code=92
    # mismatch heren; kluis.code=91
    # mismatch leeg; kluis.code=93
    # match leeg; kluis.code=94
    # non match vikinglid; kluis.code=95
    # match vikinglid; kluis.code=96
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol12','kol13']
    teller=0
    tel= Kluis.objects.all().order_by('id').first()
    mx= Kluis.objects.all().order_by('id').last()
    max=mx.id
    teller=tel.id
    print(teller)
    for m in matrix:
        for kol in range(1,10):
            a=hdr[kol]
            inh=getattr(m,a)
            kastje=getattr(m,a)
            print(teller,kastje)
            k=Kluis.objects.all().get(id=teller)
            k.kast=kastje
            k.save()
            if teller<max: teller+=1
    return

@login_required(login_url='login')
def hernummermatriks(request):
    print('in hernummermatriks===============')
    # rij=0
    # matriks regel-kolomnummering naar kolomvelden overbrengen
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol12','kol13']
    begincell=0;cellengte=0;eindcell=0
    matrix=Matriks.objects.all()
    for m in matrix:
        rij=str(m.y_as)
        cellengte=4
        regel=m.regel
        for kol in range(0,12):
            de_matriks_kolom=hdr[kol]
            # inh=getattr(m,de_matriks_kolom)
            # kastje=getattr(m,de_matriks_kolom)
            # regellengte=len(m.regel)
            # begincell=kol*cellengte
            # eindcell=0+cellengte
            # b=kol*cellengte
            # e=b+cellengte
            # c=regel[b:e] 
            oorspronkelijkmatriksnummer=decodeer(regel,de_matriks_kolom,kol,cellengte)
            print(m.naam,de_matriks_kolom,begincell,oorspronkelijkmatriksnummer)
            # print(m.naam,de_matriks_kolom,b,inh,begincell,e,c)
            try:
                vl=KluisjesRV.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
                if vl.huurders.all().count()==0:
                    oorspronkelijkmatriksnummer=' - '
            except:
                # will be part of settings
                c='---'   #set the mismatch string                                              #ON
                print('mismatch',m,de_matriks_kolom,oorspronkelijkmatriksnummer) #ON
                # c='r'+ rij + 'k' +de_matriks_kolom[3:]                   #ON
                # c=vl.row + vl.col
                setattr(m, de_matriks_kolom, c)  #puts a hit in the cell or an mismatch '---'   #ON
                # setattr(m, de_matriks_kolom, 'rij'+ rij.zfill(2) + de_matriks_kolom)          #OFF

                pass
            setattr(m, de_matriks_kolom, oorspronkelijkmatriksnummer)
            # vl.kluisje='rij'+ rij.zfill(2) + de_matriks_kolom #off when handout is true       #OFF
            # vl.row=rij.zfill(2)
            # vl.col=de_matriks_kolom[3:].zfill(2)
            # print('match',vl.col) #ON
            # setattr(m, de_matriks_kolom, 'rij'+ rij.zfill(2) + de_matriks_kolom)              #OFF
            # vl.save()
            m.save()
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
    krv= KluisjesRV.objects.all()
    l=0
    for rv in krv:
        if 'Heren' in rv.kastje:
            l=len(rv.kastje)
            if isNum(rv.kastje[6:l]):
                rv.kluisnummer='H' + rv.kastje[6:l].zfill(3)
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
                rv.topic='C' +rv.kastje[0:5]
                rv.save()
                try:
                    vl=Vikinglid.objects.get(name=rv.naamvoluit)
                    rv.huurders.add(vl.id)
                    rv.verhuurd=True
                    rv.save()
                except:
                    print(rv.naamvoluit)
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
    filter2=Q(kluisnummer__icontains=q)    
    filter3=Q(naamvoluit__icontains=q)    
    filter5=Q(topic__icontains=q)    
    kluizen=KluisjesRV.objects.all().order_by('kluisnummer').filter((filter2|filter3|filter5))
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
    csv_data=Matriks.objects.all().order_by('naam')
    # csv_data=header|csv_data
    t = loader.get_template('viking/export_matriks.txt')
    c = {'data': csv_data,'hdr':header}
    response.write(t.render(c))
    return response
#  =========== EXPORT RUBBUSH HEREAFTER ========================
def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Foo', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('viking/my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response

# class Echo:
#     """An object that implements just the write method of the file-like
#     interface.
#     """
#     def write(self, value):
#         """Write the value by returning it, instead of storing in a buffer."""
#         return value

# def some_streaming_csv_view(request):
#     """A view that streams a large CSV file."""
#     # Generate a sequence of rows. The range is based on the maximum number of
#     # rows that can be handled by a single sheet in most spreadsheet
#     # applications.
#     mtrx= Matriks.objects.all()
#     # rows = (["Row {}".format(idx), str(idx)] 
#     rows = (["mtrx".format(idx), str(idx)] 
#     # for idx in range(65536))
#     for idx in mtrx)
#     pseudo_buffer = Echo()
#     writer = csv.writer(pseudo_buffer)
#     return StreamingHttpResponse(
#         (writer.writerow(row) for row in rows),
#         content_type="text/csv",
#         headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
#     )