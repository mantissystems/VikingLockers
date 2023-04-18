from django.core.mail import send_mail
from django.template import loader
import csv
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
from .models import   Topic,Kluis,Vikinglid,Activiteit,Note,Matriks
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
    topcs = Activiteit.objects.values('type') .filter(name__icontains=q)
    template='viking/home.html'
    topics = Topic.objects.all()
    all=Vikinglid.objects.all()
    filter1=Q(name__icontains=q)    
    # vikingleden=Vikinglid.objects.all().filter(filter1 )
    vikingleden=Vikinglid.objects.all()

    if q=='Export Kluislijst':
            return redirect('export')
    if q=='Aanvraag':
            return redirect('create-aanvrage')
    leeg = Activiteit.objects.all().filter(
        # Q(name=None) | 
        Q(type='kluis'))
    leeg = Activiteit.objects.all().filter(
        Q(name=None) | 
        Q(type='kluis'))
    billable = Activiteit.objects.none()
    if q=='Kluisjes-leeg':
        template='viking/home.html'
        leeg = Activiteit.objects.all().filter(
        Q(lid_van=None) &
        Q(type='kluis')
        )
    if q=='Met Kluis':
        billable = Activiteit.objects.all().exclude(
        Q(lid_van=None)| 
        Q(type='ploeg')
        # &
        )
        template='viking/home.html'
    vikingleden=Vikinglid.objects.all()

    print('billable', billable.count())
    context = {
        'koplegen':[f'verdeling ({all.count()} leden; {leeg.count()} leeg)','lid'],
        'vikingleden':vikingleden,
        'topics': topics, 
        'topcs':topcs,
        'empty':leeg,
        'billable':billable,
        'legen':leeg.count(),
        'q':q,
        }
    kasten=Kluis.objects.all() #.filter(kast__icontains=bloknummer)
    mtrx=Matriks.objects.all()
    heren=Matriks.objects.all().filter(kol13='heren01')
    dames=Matriks.objects.all().filter(kol13='dames01')
    # rounds=nr #int(kolommen/2)
        # r = 0
        # rijen=nr # (kolommen-1)*rounds
    spelers=Vikinglid.objects.all() #.filter(nr=str(t).zfill(2)).values_list('naam')
    context={
        # 'kop': [f'matrix ({rijen}rijen) bij {kolommen} kolommen',],
            'kopmtrx' : [f'kast', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9'],#,'kol10','kol11','kol12','kol13'], 'regel-informatie kluisnummers'
            # 'regels': Matriks.objects.all(),
            'matrix': mtrx,
            'heren': heren,
            'dames': dames,
            # 'kastenn': kasten,
            #  'kopspelers': [f'matrix({rijen}rijen; {rounds} rijen) with {kolommen} kolommen'],
            # 'spelers': spelers,

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

@login_required(login_url='login')
def update_kluis(request, pk,kol):
    column=int(kol)
    print('in updpate_kluis')
    matrix=Matriks.objects.get(id=pk)
    rgl=matrix.y_as
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    vikingers=Vikinglid.objects.all().order_by('name')
    a=hdr[column];print(a)
    kluisje=getattr(matrix,a)
    # loc=getattr(matrix,hdr[13])
    context={}
    try:
        kls=Kluis.objects.filter(kast=kluisje).first()
        form=KluisjeForm(instance=kls)
        print('try:',kluisje,kls.id)
        context = {
                'form': form,
                'kluis': kls,
                'vikingers':vikingers,
            }
    except:
        kls=Kluis.objects.filter(name__icontains='leeg').first()
        form=KluisjeForm(instance=kls)
        print('except: ',kluisje,rgl,kol)
        context = {
                'form': form,
                'kluis': kls,
                'vikingers':vikingers,
            }
    if request.method == 'POST':
            huurder= request.POST.get('heeftkluis')
            if huurder:
                kls.name = huurder
                print('huurder',huurder)
                form.name = huurder #request.POST.get('huurder')
                kls.body = huurder #request.POST.get('huurder')
                # kls.kast=matrix.kol13+str(matrix.y_as)+str(kol)
                kls.location=matrix.kol13+str(matrix.y_as)+str(kol)
                kls.save()
                kolom=setattr(matrix,kluisje,'kluisje')
                # Matriks.objects.all().filter(id=pk,y_as=rgl).update(kol12='wb')
                # if column==1: matrix.kol1='d'+ str(kls.id)
                # if column==2: matrix.kol2='d'+ str(kls.id)
                # if column==3: matrix.kol3='d'+ str(kls.id)
                # if column==4: matrix.kol4='d'+ str(kls.id)
                # if column==5: matrix.kol5='d'+ str(kls.id)
                # if column==6: matrix.kol6='d'+ str(kls.id)
                # if column==7: matrix.kol7='d'+ str(kls.id)
                # if column==8: matrix.kol8='d'+ str(kls.id)
                # if column==9: matrix.kol9='d'+ str(kls.id)
            # if column==10: matrix.kol10='d'+ str(kls.id)
            # if column==11: matrix.kol11='d'+ str(kls.id)
            # if column==12: matrix.kol12='d'+ str(kls.id)
            # if column==13: matrix.kol13=kls.id
            matrix.save()

            return redirect('get_matrix')
    print(column)


    return render(request, 'viking/update_kluis_form.html', context)

class Blokken(TemplateView):
    template_name = 'viking/bloktabel_list.html'
    def get_context_data(self, **kwargs):
        bloknummer=''
        matrixnaam='dames01'
        vv=matrixnaam[0:1]
        hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9'] #,'kol10','kol11','kol12','kol13']
        # matrix=Matriks.objects.all()
        # matrix=Matriks.objects.filter(kol13='heren01').first()
        matrix=Matriks.objects.all().filter(kol13='heren01').first()
        ctx = super(Blokken, self).get_context_data(**kwargs)
        ctx['header'] = ['Rondenummer', '  Blok nummer  ', 'Paring','Thuis','Uit']
        ctx["rows"] = Kluis.objects.all()
        ctx["bloknummer"] = bloknummer
        nr=9
        kolommen = nr
        rounds=nr #int(kolommen/2)
        r = 0
        rijen=nr # (kolommen-1)*rounds
        ctx['kop'] = [f'matrix({rijen}rijen; {rounds} rijen) with {kolommen} kolommen']
        ctx["regels"]= Matriks.objects.all()
        s = ""
        w1=''
        p = 0
        # Matriks.objects.all().delete()
        for teama in range(0,kolommen):  # 0 tot 6 of 9 9
            s = ""
            p = 0
            for teamb in range(0,kolommen):
                if teama != teamb:
                    p += 1
                    ronde = (teamb + teama)%kolommen
                    if ronde == 0: ronde = kolommen
                    r+=1
                    s += vv + str(r).zfill(3) #+'|.'

                    # kls=Kluis.objects.all().get(id=r); kls.topic_id=r ; kls.code=bloknummer;  kls.save()
                    if p%2 == 0:
                        w1 += str(ronde)
                        w1 = ""
                    else:
                        r+=1
                        s += vv + str(r).zfill(3) #+'|!'
                        ronde += 1
                    # kls=Kluis.objects.all().get(id=r); kls.topic_id=r; kls.code=bloknummer;  kls.save()

                if teama == teamb:
                    r+=1
                    s +=vv +  str(r).zfill(3) #+'|='
                    # kls=Kluis.objects.all().get(id=r); kls.topic_id=r ; kls.code=bloknummer;  kls.save()

            print(s)
            # NIET MEER AANMAKEN DAT IS EENMALIG; UPDATE CEL WITH KLUIS INFO
            # VELD 'regel' bevat kluisnummering '040' = kolom 1; rij 4 
            Matriks.objects.update_or_create( 
                        kop=s,
                        regel=s,ronde=r,x_as=r,y_as=ronde,kol13=matrixnaam)
            
        # y=0
        for m in Matriks.objects.all():
            # y+=1
            print(m.id)
            for i in range(1,10):
                set_blokken(request,m.id,i,matrixnaam)
        return ctx
    
def get_matrix(request):
    template_name = 'viking/bloktabel_list.html'
    nr=9
    kolommen = nr
    kasten=Kluis.objects.all() #.filter(kast__icontains=bloknummer)
    mtrx=Matriks.objects.all()
    heren=Matriks.objects.all().filter(kol13='heren01')
    dames=Matriks.objects.all().filter(kol13='dames01')
    rounds=nr #int(kolommen/2)
    # r = 0
    rijen=nr # (kolommen-1)*rounds
    spelers=Vikinglid.objects.all() #.filter(nr=str(t).zfill(2)).values_list('naam')
    context={'kop': [f'matrix ({rijen}rijen) bij {kolommen} kolommen',],
            'kopmtrx' : [f'kast', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9'],#,'kol10','kol11','kol12','kol13'], 'regel-informatie kluisnummers'
            # 'regels': Matriks.objects.all(),
            'matrix': mtrx,
            'heren': heren,
            'dames': dames,
            # 'kastenn': kasten,
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
        b=(col-1)*3
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
        # set_blokken(request,pk,col)   #matriks regel, matriks kolom
        # matrix.save()
        # matrix.kol1=new_cell_content
        # matrix.save()
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

def modify_matriks( matriksregel,matrikskolom:int,cel_inhoud):
    print('in modify_matriks')
    matrix=Matriks.objects.get(y_as=matriksregel)
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12'] #,'kol12','kol13']
    a=hdr[matrikskolom]
    k=getattr(matrix,a)
    print(k)
    # pos=matrikskolom;begincell=0;cellengte=0;eindcell=0
    cellengte=3
    col=matrikskolom
    regellengte=len(matrix.regel)
    new_cell_content=cel_inhoud
    if col in (1,2,3,4,5,6,7,8,9,10,11,12,13): #om te voorkomen dat er verkeerde kolomnummers binnenkomen
        
        b=(col-1)*3
        e=b+3
        if len(cel_inhoud) > 3:
            new_cell_content=cel_inhoud[0:3]
        else:
            c=matriksregel[b:e] 
            new_info=c
            new_cell_content=c 
        print(matriksregel,'col', matrikskolom,'cel',cel_inhoud,k)
        print('uit modify_matriks')
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
        matrix.kol13='Heren' #new_cell_content
        matrix.save()
    return

def set_blokken(request, pk,kol,matrixnaam):
    kls=Kluis.objects.get(id=kol)
    # matrix=Matriks.objects.filter(kol13__icontains='heren').first()
    matrix=Matriks.objects.get(id=pk)
    hdr=[ 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12'] #,'kol12','kol13']
    a=hdr[int(kol)]
    col=int(kol)
    k=getattr(matrix,a)
    print('in set_blokken')
    # return
    pos=int(kol);begincell=0;cellengte=0;eindcell=0
    cellengte=4
    regellengte=len(matrix.regel)
    begincell=col+pos*cellengte
    eindcell=0+cellengte
    regel=matrix.regel
    cell=regel[begincell:eindcell]
    rechts=regel[eindcell+cellengte:regellengte]
    new_cell_content=' xxx'
    if col in (1,2,3,4,5,6,7,8,9,10,11,12,13): #om te voorkomen dat er verkeerde kolomnummers binnenkomen
        b=(col-1)*cellengte
        e=b+cellengte
        c=regel[b:e] 
        new_info=c
        new_cell_content=c 
        print(regellengte,'col', col,'cel',c)

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
    # if col==13: matrix.kol13='Heren' #new_cell_content
    matrix.kol13=matrixnaam +'!' #new_cell_content
    kluisje=getattr(matrix,a)
    kolom=setattr(matrix,kluisje,'kluisje')

    matrix.save()
    return

def check_matriks(request):
    print('in check_matriks')
    matrix=Matriks.objects.all()
    kluis=Kluis.objects.all().update(code='')
    # doorloop alle velden
    # 1.controleer: dame in dames; heer in heren
    # mismatch dames; kluis.code=92
    # mismatch heren; kluis.code=91
    # mismatch leeg; kluis.code=93
    # match leeg; kluis.code=94
    # non match vikinglid; kluis.code=95
    # match vikinglid; kluis.code=96
    # hit met kluis.kast; kluis.code +=teller
    # kls=Kluis.objects.get(id=kol)
    # matrix=Matriks.objects.filter(kol13__icontains='heren').first()
    hdr=[ 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol12','kol13']
    teller=0
    for m in matrix:
        teller+=1
        for k in range(0,13):
            a=hdr[k]
            inh=getattr(m,a)
            kluis=Kluis.objects.all().filter(kast=inh).first()
            if kluis:
                lid=Vikinglid.objects.all().filter(name=kluis.name).first()
                if lid:
                    print(inh,kluis.name,lid.name)
                    kluis.code=96
                if kluis.name=='leeg':
                    kluis.code=93
                else:
                    kluis.code=str(teller)
                kluis.save()
            else:   #matriks has no match with kluis.kast 
                kluis = Kluis.objects.all().filter(
                Q(code=None) |
                Q(code='') 
                ).first() #skip kluis.code blank
                kluis.code=95
                kluis.save()
                print('code=blank')
    context={}
    # return
    return render(request, 'viking/home.html', context)


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
    topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, 'viking/topics.html', {'topics': topics})