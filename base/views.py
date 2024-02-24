import csv
from typing import Any
from django.contrib import messages
from django import forms
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from base.models import Areset,Message,User,Topic,Locker,Ploeg,Helptekst,Bericht,Excellijst,Person,Facturatielijst,Tijdregel
from django.db.models import Q
from base.forms import RoomForm, UserForm,  MyUserCreationForm,LockerForm,ExcelForm,PersonForm,WachtlijstForm,LockerFormAdmin,FormatForm
from django.views.generic import(TemplateView,ListView,FormView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.db import connection
from collections import namedtuple
from rest_framework import status
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.utils import formats
from django.core.mail import EmailMessage
from django.core import mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.template.loader import render_to_string  #for email use
from .admin import LockeradminResource,PersonadminResource
from .resources import LockerResource,PersonResource

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        username=request.POST.get('email').lower()

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            url = "/berichten/" + "?q=" + "'controleer  wachtwoord en/of het emailadres'"
            return HttpResponseRedirect(url)
            # messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    pemail=request.POST.get('email')
    print(pemail)
    try:
        usr=User.objects.get(email=pemail)
    except:
        pass
    else:
        messages.error(request, 'User email already in use.')


    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            print(user.username)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print('else')
            url='/berichten'
            messages.add_message(request, messages.ERROR, "3.An error occurred during registration", extra_tags="dragonball")
            return HttpResponseRedirect(url)

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    lijst='home'
    system_messages = messages.get_messages(request)
    for message in system_messages:
     print()
    # This iteration is necessary to clear messages
     pass
    messages.set_level(request, messages.INFO)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    qq=q.lower()
    A=Q(email__icontains='vrij')
    B=Q(email__icontains='onbekend')
    B=Q(email__icontains='wachtlijst')
    C=Q(obsolete=True)
    D=Q(opgezegd=True)
    onverhuurd =Locker.objects.all().filter(  A | B  | C | D ).order_by('locker')
    verhuurd =Locker.objects.filter(
        (Q(verhuurd=True)
        ) 
    ).order_by('locker')

    lockers =Locker.objects.filter(
    Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q)&
    Q(verhuurd=True)
    ).order_by('locker')# .exclude(id__in=onverhuurd_lijst)
    messagelocker=Locker.objects.all().first()    
    entrants_in=lockers
    rest=verhuurd.count() - onverhuurd.count() 
    if request.method == 'POST':
            message = Bericht.objects.create(
            user=request.user,
            locker=messagelocker,
            body=request.POST.get('body')
        )
    if not request.user.is_authenticated:
        print('1.not-auth:', request.user)
        count=9
        url = "/berichten/"
        qs_in=Locker.objects.all().filter(verhuurd=True)
        qs_outd=Locker.objects.all().filter(verhuurd=False,kluisnummer__icontains='dames').exclude(obsolete=True).exclude(opgezegd=True)
        qs_outh=Locker.objects.all().filter(verhuurd=False,kluisnummer__icontains='heren').exclude(obsolete=True).exclude(opgezegd=True)
        messages.add_message(request, messages.INFO, "Welkom bij Viking Lockers.")    
        messages.add_message(request, messages.INFO, f"{qs_in.count()} lockers bezet.")    
        messages.add_message(request, messages.INFO, f"{qs_outh.count()} bij Heren onbezet.")    
        messages.add_message(request, messages.INFO, f"{qs_outd.count()} bij Dames  onbezet.")    
        messages.add_message(request, messages.INFO, f"Vraag een locker aan via vikinglockers@mantisbv.nl")    
        messages.add_message(request, messages.ERROR, "U bent niet ingelogd. Svp Inloggen / Registreren", extra_tags="dragonball")
        return HttpResponseRedirect(url)
    if request.user.is_authenticated:
        print('1.authorised:', request.user)
    messages.add_message(request, messages.INFO, "Welkom bij Lockermanager", extra_tags="dragonball")

    storage = messages.get_messages(request)
    if 'xls' in qq:
        x = qq.replace("xls ", "")
        q=x
        queryset = Excellijst.objects.filter(
        Q(email__icontains=q)|
        Q(type__icontains=q)|
        Q(excel__icontains=q)|
        Q(kluisnummer__icontains=q)
        ).order_by('kluisnummer')
        url = "excellijst" + "?q=" +q 
        return HttpResponseRedirect(url)
    elif 'fact' in qq:
        x = qq.replace("fact ", "")
        # print(x)
        q=x
        url = "facturatielijst" + "?q=" +q 
        return HttpResponseRedirect(url)
    elif 'pers' in qq:
        x = qq.replace("pers ", "")
        q=x
        url = "profiles" + "?q=" +q 
        return HttpResponseRedirect(url)
    elif 'usr' in qq:
        x = qq.replace("usr ", "")
        q=x
        url = "users" + "?q=" +q 
        return HttpResponseRedirect(url)

    else:
        print('else:',q)
        url = "lockerview"  + "?q=" +q
        return HttpResponseRedirect(url)

class LockerView (LoginRequiredMixin,ListView):
    login_url='login'
    model=Locker
def get_context_data(self, **kwargs):
        context = super(LockerView, self).get_context_data(**kwargs)
        return context

def get_queryset(self): # new
    users_found=User.objects.all().values_list('email',flat=True)
    queryset = Locker.objects.filter(
        Q(verhuurd=True)&
        Q(email__in=users_found) 
    ).order_by('-updated','locker')
    return queryset
paginate_by = 10
def get_context_data(self, **kwargs):
        context = super(LockerView, self).get_context_data(**kwargs)
        return context
 
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def helpPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    aantalusers=User.objects.all()
    results = (Locker.objects
    .values('kluisnummer')
    .annotate(dcount=Count('kluisnummer'))
    .order_by()
    )   
    verhuurd =Locker.objects.filter(
        (Q(verhuurd=True)
        ) 
        ).order_by('locker')
    A=Q(email__icontains='vrij')
    B=Q(email__icontains='bekend')
    C=Q(obsolete=True)
    D=Q(opgezegd=True)
    E=Q(email__icontains='--')
    F=Q(email__icontains='==')
    onverhuurd =Locker.objects.all().filter( A | B |  C | D | E | F ).order_by('locker')
    messages.add_message(request, messages.INFO, f"{aantalusers.count()}", extra_tags="dragonball")

    helptekst=Helptekst.objects.filter(
            Q(title__icontains=q)|
            Q(content__icontains=q)
        ).order_by('seq').exclude(publish=False)
    return render(request, 'base/helptekst.html', {'helptekst': helptekst,'aantalusers':verhuurd,'onverhuurd': onverhuurd,'onverhuurd':onverhuurd})


def infoPage(request):
    page = 'info'
    room_messages = Message.objects.all()
    fverhuurd=Q(verhuurd=True)
    if request.user != AnonymousUser:
        user=User.objects.first()
        yourlockers=Locker.objects.filter(
            Q(email__icontains=user.email)|
            Q(verhuurd=True)
        )
        page=''
        print('infoPage cnt..', yourlockers.count())
    verhuurd=Locker.objects.all().filter(fverhuurd)  #verzamel verhuurde kluisjes voor de room 
    header_logged_in='U huurt bij ons: '
    header='Verhuurd: '
    context={'room_messages': room_messages,
             'yourlockers':yourlockers,
             'header':header,
             'header_logged_in':header_logged_in,
             'page':page,
             }
    return render(request, 'base/info.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    berichten=Bericht.objects.all().filter(user=request.user.id)
    team='nieuw'
    context = {
                'berichten':berichten,
                'form': form,
            }
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if user.locker == 'xx':
                messages.success(request, f'Uw locker opheffen?: {user.locker}')
                print('locker opheffen?')
            ploeg, created = Ploeg.objects.get_or_create(name=team)
            locker, created = Locker.objects.update_or_create(kluisnummer=user.locker,
                                                           email=user.email,
                                                           kluisje=user.locker)
            try:
                teambestaatal = Ploeg.objects.filter(name=user.ploeg)
            except: 
                Ploeg.DoesNotExist
                url = reverse('update-user')
                ploeg, created = Ploeg.objects.get_or_create(name=team)
                # messages.error(request, f'1 Teamleider per ploeg  {user.ploeg} wordt niet aangemaakt of was reeds aangemaakt tijdens registratie')
                return HttpResponseRedirect(url)
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html', context)

class CreateUser(CreateView):
    model = User
    fields = ['first_name','email',]
    # fields='__all__'
    success_url = reverse_lazy('home')
    # print('usercreateview')
    def form_valid(self, form):
        messages.success(self.request, "Wijzigingen in user zijn opgeslagen.")
        return super(CreateUser,self).form_valid(form)

class EditUser( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = User
    form_class=UserForm
    template_name='base/user_form.html'
    # initial = {"key": "value"}
    print('in userupdate')
    success_url = reverse_lazy('users')
    
    def get_object(self):
        print('in get_object')
        _id = self.request.GET.get('pk') if self.request.GET.get('pk') != None else ''
        print(_id)
        obj = get_object_or_404(User, id=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        print('in get_context_data')
        context = super().get_context_data(**kwargs)
        context["lockers"] = User.objects.all()
        obj = super().get_object(**kwargs)
        return context
    
    def form_valid(self, form):
        print('in form_valid')
        messages.success(self.request, "The User was updated successfully.")
        success_url = reverse_lazy('users')
        return super(EditUser,self).form_valid(form)

class updateUser3(LoginRequiredMixin,UpdateView):
    login_url='login'
    model = User
    # fields='__all__'
    fields = ['username','first_name','email','locker']
    success_url = reverse_lazy('users')
    def get_object(self):
        # obj = get_object_or_404(Locker, kluisnummer__slug=self.kwargs['pk'], slug=self.kwargs['pk'] )
        obj = get_object_or_404(User, id=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        kluis = form.cleaned_data['locker']  
        email = form.cleaned_data['email'] 
        messages.success(self.request, "The user was updated successfully.")
        return super(updateUser3,self).form_valid(form)
        
class updateUser_email(LoginRequiredMixin,UpdateView):
    login_url='login'
    model = Locker
    fields='__all__'
    # fields = ['username','email','locker']
    success_url = reverse_lazy('users')
    def get_object(self):
        print(self.kwargs['kluis'])
        obj = get_object_or_404(Locker, kluisnummer=self.kwargs['kluis'],)# slug=self.kwargs['kluis'] )
        return obj
    def get_context_data(self,**kwargs):
        locker=self.get_object()
        print(locker)
        form = LockerForm(instance=locker)
        context = {
            'form': form,
            }
        return context

    def form_valid(self, form):
        kluis = form.cleaned_data['kluisnummer']  
        email = form.cleaned_data['email'] 
        if kluis:
            print(kluis)
        else:
                    messages.success(self.request, "Something went wrong.")
        messages.success(self.request, "The locker was updated successfully.")
        return super(updateUser_email,self).form_valid(form)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    lockers = Locker.objects.all()
    topics = Topic.objects.all()
    context = {'user': user,
               'room_messages': topics,
                 'topics': topics,
                 'lockers':lockers,
                }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def myProfile(request):
    user = request.user
    form = UserForm(instance=user)
    berichten=Bericht.objects.all().filter(user=request.user.id)
    locker= request.POST.get('locker')
    context = {
                'berichten':berichten,
                'form': form,
                'locker': locker,
            }
    if request.method == 'POST':
                # fields = ['avatar', 'name', 'username','locker', 'email']
        form.name=request.POST.get('name')
        form.name=request.POST.get('name')
        form.email=request.POST.get('email')
        form.locker=request.POST.get('locker')
        form.verhuurd=False
        if request.POST.get('locker'):
            print('requested', request.POST.get('locker'))            
            locker, created = Locker.objects.update_or_create(
            kluisnummer=request.POST.get('locker'),
            email=request.POST.get('locker'),
            verhuurd=False,
            kluisje=request.POST.get('locker'))
        if not form.is_valid():
            print('invalid')
        if form.is_valid():
            locker, created = Locker.objects.update_or_create(
            kluisnummer=request.POST.get('locker'),
            email=user.email,
            verhuurd=False,
            kluisje=request.POST.get('locker'))
            form.save()
            return redirect('update-profile', pk=user.id)
    return render(request, 'base/update-profile.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def user_listPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(name__icontains=q)
    return render(request, 'base/user_list.html', {'users': users})

def excelPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lijst='excellijst'
    menuoptie='bijwerken'
    lockers = Excellijst.objects.filter(kluisnummer__icontains=q)
    if request.method == 'POST':
        qs=Facturatielijst.objects.all()
        for f in qs:
            if User.objects.filter(email=f.email).exists():
                f.is_registered='registered'
                f.save()
            elif Excellijst.objects.filter(email=f.email).exists():
                f.in_excel='in_excel'
            elif  '--' in f.kluisnummer:
                f.type='vrij'
                f.save()
            # else:
            #     f.save()
            
        lockers = Excellijst.objects.filter(kluisnummer__icontains=q)
        return redirect('home')
    return render(request, 'base/delete.html', {'lockers': lockers,'excellijst':lijst,'menuoptie':menuoptie})

def profilePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    profiles = Person.objects.all() #filter(name__icontains=q)
    return render(request, 'base/profiles.html', {'profiles': profiles})

def excel_regelPage(request,pk):
    excel = Excellijst.objects.get(id=pk)
    form = ExcelForm(instance=excel)
    lockers=Excellijst.objects.all()
    # topics=Topic.objects.all()
    vikingers=User.objects.all().order_by('username')
    context = {
                'vikingers':vikingers,
                'kluis': excel,
                'form': form,
            }    
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES, instance=excel)
        onderhuurder= request.POST.get('onderhuurder')
        slotcode= request.POST.get('code')
        type= request.POST.get('type')
        kluis= request.POST.get('kluisnummer')
        sleutels= request.POST.get('sleutels')
        huuropheffen= request.POST.get('huuropheffen')
        print('onderhuurder',kluis, onderhuurder,sleutels,slotcode)
        if form.is_valid():
            print('form is valid')
            if onderhuurder:
                print('onderhuurder', onderhuurder)
                h=User.objects.get(id=onderhuurder)
                return redirect('locker', kluis.id)
            if huuropheffen:

                h=User.objects.get(id=huuropheffen)
                print('opheffen',h)
                form.save()
            return redirect('excel-regel', kluis.id)
    return render(request, 'base/excellijst_form.html', context)

class MemberListView (LoginRequiredMixin, ListView):
    login_url='login'
    model=User
    def get_context_data(self,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        if query == None: query=""
        queryset = User.objects.filter(
            Q(email__icontains=query)|
            Q(username__icontains=query)|
            Q(locker__icontains=query)
            ).order_by('email')
        context = {
            'query': query,
            'object_list' :queryset,
            }
        return context
paginate_by = 20

class PersonListView(ListView,FormView):
    model=Person
    template_name='base/person_list.html'
    form_class=FormatForm
    context_object_name = "person_list"

    def get_queryset(self) :
        queryset=Person.objects.all() #.filter(verhuurd=True).order_by('topic')
        return queryset
    
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        print('in personlistview get_context_data:',q)
        s='base_person';l=len(s)+1
        headers=Person.objects.all().query.get_meta().fields 
        fields=['id','name','email','onderhuur','wachtlijst','hoofdhuurder','onderhuur','locker','tekst']
        header=[]
        for k in headers:
            if str(k)[l:] in fields:
                header.append(str(k)[l:])              

        obs= Q(obsolete=True)
        context = super().get_context_data(**kwargs)
        qs_in=Person.objects.all().order_by('name')
        context["persons_in"] = qs_in
        self.object_list = qs_in
        context["header"] = header
        context["table"] = s
        return context

    def post(self,request,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        qs =Person.objects.all()
        data_set=PersonadminResource().export(qs)
        format=request.POST.get('format')
        print(format,'xxxx->')
        if format=='xls': ds=data_set.xls
        elif format=='csv': ds=data_set.csv
        else: 
            ds=data_set.json
        response=HttpResponse(ds,content_type=f"{format}")
        response['Content-Disposition'] = f"attachment;filename=persons.{format}"
        return response
    
# ---------------------------------------------------------------------------
class TimesheetView(ListView,FormView):
    model=Areset
    template_name='base/areset_list.html'
    form_class=FormatForm
    success_url = reverse_lazy('t3')
    context_object_name = "person_list"

    def get_queryset(self) :
        queryset=Areset.objects.all() #.filter(verhuurd=True).order_by('topic')
        return queryset
    
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        print('in personlistview get_context_data:',q)
        s='base_areset';l=len(s)+1
        headers=Areset.objects.all().query.get_meta().fields 
        fields=['id','name','description','updated','created','host','status']
        header=[]
        for k in headers:
            if str(k)[l:] in fields:
                header.append(str(k)[l:])              
        context = super().get_context_data(**kwargs)
        qs_in=Areset.objects.all().order_by('name')
        context["timesheets"] = qs_in
        self.object_list = qs_in
        context["header"] = header
        context["table"] = s
        return context

@login_required(login_url='login')
def createAreset(request):
    form = RoomForm()
    topics = Topic.objects.all()
    werk=Areset.objects.all()
    for w in werk:
        print(w.name)
    user=User.objects.get(is_superuser=True)
    if request.method == 'POST':
        topic_name = request.POST.get('topic') #het is default Autoreset
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Areset.objects.create(
            # host=user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('t3')
    context = {'form': form, 'topics': topics,'werk':werk}
    return render(request, 'base/room_form.html', context)
# ---------------------------------------------------------------------------

def areset(request, pk):
    room = Areset.objects.get(id=pk)
    tijdregels=Tijdregel.objects.all().filter(tijdregel=room)
    header=[]
    s='base_areset';l=len(s)+1
    headers=Areset.objects.all().query.get_meta().fields 
    fields=['id','name','description','updated','created','host','status']
    for k in headers:
        if str(k)[l:] in fields:
            header.append(str(k)[l:])              

    header2=[]
    t='base_tijdregel';l=len(t)+1
    headers2=Tijdregel.objects.all().query.get_meta().fields 
    fields2=['id','status','begin','einde','created','updated']
    for k in headers2:
        if str(k)[l:] in fields2:
            header2.append(str(k)[l:])              

    # print(header,header2)
    if request.method == 'POST':
        s='base_areset';l=len(s)+1
        headers=Areset.objects.all().query.get_meta().fields 
        fields=['id','name','description','updated','created','host','status']
        return redirect('t2', pk=room.id)

    context = {'room': room, 'header':header,'header2':header2,
               'tijdregels': tijdregels}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def deleteaReset(request, pk):
    room = Areset.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('t3')
    return render(request, 'base/delete.html', {'obj': room})

def room_start(request,pk):
    usr=request.user
    now = timezone.now()
    url = reverse('home')
    print('startwerk')
    m=Areset.objects.get(id=pk)
    if not m.status=='end':
        m.status='start'
        m.save()
    if Tijdregel.objects.filter(tijdregel=m.id,status='start').exists():
        t=Tijdregel.objects.get(tijdregel=m.id,status='start')
        print('niet aan te mmaken',m)
        t.status='start'
        t.begin=now, 
        t.einde=now, 
        t.save()
        
    else:
        try:
            t=Tijdregel.objects.get(tijdregel=m.id,status='start')
        except:
            Tijdregel.DoesNotExist
            print('aan te maken',m)
            t=Tijdregel.objects.update_or_create(
                status='start',
            begin=now, 
            einde=now, 
                tijdregel=m,
            )
        finally:
            print('aangemaakt',m)
    return HttpResponseRedirect(reverse('t2', args=(m.id,)))

def vervolg(request):
    import datetime
    usr=request.user
    now=  datetime.date.today()
    url = reverse('home')
    print('startwerk')
    m=Areset.objects.latest('updated')
    if not m.status=='end':
        m.status='start'
        m.save()
    if Tijdregel.objects.filter(tijdregel=m.id,status='start').exists():
        tr= Tijdregel.objects.filter(tijdregel=m.id,status__icontains='vervolg')
        trc=tr.count()
        vg=Tijdregel.objects.filter(updated__isnull=False).latest('updated')
        vlg=Tijdregel.objects.latest('begin')
        vlg.begin=now
        vlg.save()
        Tijdregel.objects.update_or_create(
         status='vervolg' + str(trc),
            begin=now, 
            einde=now, 
            tijdregel=m,
    )
    return HttpResponseRedirect(url)

def stop(request):
    usr=request.user
    name=''
    now = timezone.now()

    url = reverse('t3')
    print('eindewerk')
    m=Areset.objects.latest('updated')
    if Tijdregel.objects.filter(tijdregel=m.id,status='stop').exists():
        print('niet aanmmaken',m)
        if not m.status=='end':
            m.status='stop'
            m.save()
    if Tijdregel.objects.filter(tijdregel=m.id,status='stop').exists():
        v=Tijdregel.objects.latest('updated')
        v.status='stop'
        v.begin=now, 
        v.einde=now, 
        v.save()

    else:
        # Tijdregel.DoesNotExist
        print('aan te maken',m)
        t=Tijdregel.objects.update_or_create(
            status='stop',
            begin=now, 
            einde=now,
            tijdregel=m,
        )
        print('aangemaakt',m)
    return HttpResponseRedirect(url)

def clear_tijdregels(request,pk):
    url = reverse('t3')
    m=Areset.objects.get(id=pk)
    m.status='clear'
    m.save()
    if request.method == 'POST':
        Tijdregel.objects.all().filter(tijdregel=m).delete()
        return HttpResponseRedirect(url)
    return render(request, 'base/delete.html', {'obj': m})

def end(request):
    usr=request.user
    msg=''
    m=''
    name=''
    now = timezone.now()
    url = reverse('t3')
    # print('eindewerk')
    m=Areset.objects.latest('updated')
    if not m.status=='end':
        m.status='end'
        m.save()
    return HttpResponseRedirect(url)

def update_vervolg(request,pk):
    import datetime
    usr=request.user
    now=  datetime.date.today()
    url = reverse('t3')
    # print('startwerk')
    m=Areset.objects.get(id=pk)
    if not m.status=='end':
        m.status='start'
        m.save()
    if Tijdregel.objects.filter(tijdregel=m.id,status='start').exists():
        tr= Tijdregel.objects.filter(tijdregel=m.id,status__icontains='vervolg')
        trc=tr.count()
        vg=Tijdregel.objects.filter(updated__isnull=False).latest('updated')
        vlg=Tijdregel.objects.latest('begin')
        vlg.begin=now
        vlg.save()
        Tijdregel.objects.update_or_create(
         status='vervolg' + str(trc),
            begin=now, 
            einde=now, 
            tijdregel=m,
    )
    return HttpResponseRedirect(reverse('t2', args=(m.id,)))
    # return HttpResponseRedirect(url)

class PersonListView_old (ListView):
    model=Person
    def get_context_data(self,**kwargs):
        
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        if query == None: query=""
        print('query',q)
        queryset = Person.objects.filter(
            Q(email__icontains=query)|
            Q(name__icontains=query)|
            Q(locker__icontains=query)
            ).order_by('hoofdhuurder','wachtlijst','onderhuur','email')
        # queryset=Person.objects.all().order_by('hoofdhuurder','wachtlijst','onderhuur','email')
        context = {
            'query': query,
            'object_list' :queryset,
            }
        return context
class Wachtlijst (ListView):
    model=Person
    template_name='base/wachtlijst.html'
    def get_context_data(self,**kwargs):
        
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        if query == None: query=""
        print('query',q)
        queryset = Person.objects.filter(
            (Q(email__icontains=query)|
            Q(name__icontains=query)|
            Q(locker__icontains=query))&Q(wachtlijst=True)
            ).order_by('kamer','created','email')
        berichten=Bericht.objects.all()
        context = {
            'query': query,
            'berichten': berichten,
            'object_list' :queryset,
            }
        return context

class RequestView (ListView):
    model=Bericht
    template_name='base/requests.html'
    def get_context_data(self,**kwargs):
        
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        if query == None: query=""
        # print('query',q)
        berichten=Bericht.objects.all().filter(
            Q(body__icontains=query)|
            Q(id=query)
            )
        context = {

            'query': query,
            'berichten': berichten,
            }
        return context

class ExcelView (LoginRequiredMixin, ListView):
    login_url='login'
    print('in excelview')
    model=Excellijst
    template_name='base/excellijst_list.html'
    paginate_by=14
    queryset=Excellijst.objects.all() 

    def get_context_data(self,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        print(query)
        if query == None: query=""
        # queryset=Excellijst.objects.all().filter(email__icontains=query)
        queryset = Excellijst.objects.all().filter(
            Q(email__icontains=query)|
            Q(type__icontains=query)|
            Q(excel__icontains=query)|
            Q(kluisnummer__icontains=query)
            ).order_by('kluisnummer')
        context = {
            'query': query,
            'object_list' :queryset,
            }
        return context
class FacturatieView (LoginRequiredMixin, ListView):
    login_url='login'
    print('in facturatieview')
    model=Excellijst
    template_name='base/facturatielijst_list.html'
    paginate_by=14
    queryset=Facturatielijst.objects.all() 

    def get_context_data(self,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        # print(query)
        if query == None: query=""
        queryset = Facturatielijst.objects.all().filter(
            Q(email__icontains=query)|
            Q(renum__icontains=query)|
            Q(kluisnummer__icontains=query)
            ).order_by('renum')
        # print(queryset.query)
        check=Facturatielijst.objects.all().exclude(type__icontains='--')
        context = {
            'query': query,
            'check': check,
            'object_list' :queryset,
            }
        return context

class PersonUpdate_id( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Person
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tekst'].label = 'Namen  Medegebruikers'
        form.fields['wachtlijst'].label = 'Wel / Niet wachtlijst'
        return form    
    fields='__all__'
    success_url = reverse_lazy('wacht-lijst')
    
    def form_valid(self, form):
        kluis ='wachtlijst'
        hoofdhuurder = form.cleaned_data['hoofdhuurder']  
        name = form.cleaned_data['name']  
        onderhuurder = form.cleaned_data['onderhuur']  
        tekst = form.cleaned_data['tekst']  
        messages.success(self.request, "The person was updated successfully.")
        success_url = reverse_lazy('wacht-lijst')
        return super(PersonUpdate_id,self).form_valid(form)
  

class EditFactuur( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Facturatielijst
    fields = ['kluisnummer','email','in_excel','is_registered','sleutels','obsolete']
    # fields = '__all__'
    success_url = reverse_lazy('facturatielijst')
    
    def form_valid(self, form):
        # kluis = form.cleaned_data['locker']  
        # email = form.cleaned_data['email'] 
        return super(EditFactuur,self).form_valid(form)
        messages.success(self.request, "The person was updated successfully.")

class PersonUpdate(UpdateView):
    model = Person
    fields = ['name','hoofdhuurder', 'email','wachtlijst','onderhuur']
    success_url = reverse_lazy('profiles')
    
    def form_valid(self, form):
        hoofdhuurder = form.cleaned_data['hoofdhuurder']  
        name = form.cleaned_data['name']  
        onderhuurder = form.cleaned_data['onderhuur']  
        wachtlijst = form.cleaned_data['wachtlijst']  
        email = form.cleaned_data['email'] 
        print(onderhuurder)
        url = reverse('delete-person', kwargs={'pk': super().person.id})
        viking= name.replace(" ", "")
        string='pbkdf2_sha256$390000$MbAy3r2ahV6QE6xFilyWG5$Hkuz0s9MNtjJ066lD0v9N2tnUv2ZuZLALt2rIL1QSAQ='
            #  viking123
        if Person.objects.filter(email=email).exists(): 
            return HttpResponseRedirect(url)
                # return HttpResponseRedirect('/delete-person/')

        if Person.objects.filter(username=viking).exists():
              return HttpResponseRedirect(url)
            # return HttpResponseRedirect('/delete-person/')
        if onderhuurder:
            print('maak een user aan van type onderhuurder')
            user=User.objects.update_or_create(username=viking,
                                                           email=email,
                                                           is_active=True,
                                                           first_name=name,
                                                           last_name=name,
                                                           password=string,
                                                           )
            # print(user)
            return HttpResponseRedirect('/delete-person/')
        return super(PersonUpdate,self).form_valid(form)
        messages.success(self.request, "The person was updated successfully.")
        return super(PersonUpdate,self).form_valid(form)
    
class PersonDeleteView(DeleteView):
    model = Person
    success_url ="/"
    template_name = "base/delete.html"

class UserDeleteView(DeleteView):
    model = User
    success_url ="/"
    template_name = "base/delete.html"

class LockerDeleteView(DeleteView):
    model = Locker
    success_url ="/"    
    template_name = "base/delete.html"

class FactuurDeleteView(DeleteView):
    model = Facturatielijst
    success_url ="/"    
    template_name = "base/delete.html"
    def get_object(self):
        obj = get_object_or_404(Facturatielijst, id=self.kwargs['pk'])
        _id = self.request.GET.get('pk') if self.request.GET.get('pk') != None else ''
        return obj


def m2mtotext(request,):
    string='pbkdf2_sha256$390000$MbAy3r2ahV6QE6xFilyWG5$Hkuz0s9MNtjJ066lD0v9N2tnUv2ZuZLALt2rIL1QSAQ='
    for l in Locker.objects.all():
        if l.email:
            if '@' in l.email and l.verhuurd==True:
                try:
                    u=User.objects.get(email=l.email)
                    # print(u.email)
                except:
                    if not 'viking' in l.email or l.obsolete==False or l.opgezegd==False:                        
                        print('geen user', l.email)
                        user=User.objects.update_or_create(username=l.email,
                                                           email=l.email,
                                                           is_active=True,
                                                           first_name=l.email,
                                                           last_name=l.email,
                                                           locker=l.kluisnummer,
                                                           password=string,
                                                           )
                        print('created ',user)
                    pass
    url = reverse('users',)
    return HttpResponseRedirect(url)

def m3(request,):
    for u in User.objects.all():
        if u.email:
            if '@' in u.email:
                try:
                    l=Locker.objects.get(email=u.email)
                    u.locker=l.topic
                    u.save()
                except:
                    print('geen huurder', u.email)
                    pass

    url = reverse('users',)
    return HttpResponseRedirect(url)
def m5(request,):
    for f in Facturatielijst.objects.all():
        if f.email:
            if '@' in f.email:
                try:
                    l=Locker.objects.get(email=f.email)
                    f.type=l.topic
                    f.sleutels=l.sleutels
                    f.save()
                except:
                    Locker.DoesNotExist
                    print('factuur geen locker', f.email)
                    pass

    url = reverse('facturatielijst',)
    return HttpResponseRedirect(url)

def m4(request,):
    for l in Locker.objects.all():
        # if l.email:
        if '@' in l.email :
                # prepare for password reset of users
            # if 'viking' in l.email: # or l.obsolete==False or l.opgezegd==False:                        
                print('onbekend of vrij', l.email)
                l.email='onbekend of vrij'
                # l.save()
    url = reverse('onverhuurd',)
    return HttpResponseRedirect(url)

def m6(request,pk):
    string='pbkdf2_sha256$390000$MbAy3r2ahV6QE6xFilyWG5$Hkuz0s9MNtjJ066lD0v9N2tnUv2ZuZLALt2rIL1QSAQ='
    l=Locker.objects.get(id=pk)
    if '@' in l.email:
        print(l.email)
        try:
            u=User.objects.get(email=l.email)
            # User.password=string
            # User.ploeg='viking'
            # User.save()
        except:
            User.DoesNotExist
            print('geen hit')
        finally:
            u.password=string
            u.ploeg='viking'
            u.save()

    url = reverse('home',)
    return HttpResponseRedirect(url)

class CreateFactuur(CreateView):
    model = Facturatielijst
    fields = ['kluisnummer','email',]
    # fields='__all__'
    success_url = reverse_lazy('facturatielijst')
    
    def form_valid(self, form):
        messages.success(self.request, "U bent op de wachtlijst geplaatst.")
        return super(CreateFactuur,self).form_valid(form)
    
class CreateLocker(CreateView):
    model = Locker
    fields = ['kluisnummer','email','verhuurd']
    # fields='__all__'
    success_url = reverse_lazy('facturatielijst')
    def __init__(self, **kwargs):
    # Go through keyword arguments, and either save their values to our
    # instance, or raise an error.
        for key, value in kwargs.items():
            print(key)
            setattr(self, key, value)

    def form_valid(self, form):
        # messages.success(self.request, "U bent op de wachtlijst geplaatst.")
        return super(CreateLocker,self).form_valid(form)


class CreatePerson(CreateView):
    model = Person
    fields = ['name','email',]
    # fields='__all__'
    # success_url = reverse_lazy('wacht-lijst')
    model = Person

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['name'].label = "Naam / Bijnaam"
        form.fields['email'].label = 'E-mail address'
        return form

    # fields = '__all__'
    fields=['name','email',]
    success_url = reverse_lazy('wacht-lijst')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']  
        email = form.cleaned_data['email'] 
        messages.success(self.request, "U bent op de wachtlijst geplaatst.")
        # wachtlijst=Locker.objects.get(kluisnummer='wachtlijst')
        return super(CreatePerson,self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'email of naam reeds in gebruik', 'warning')
        # url = "/berichten/" + "?q=" + form.fields['email']
        return HttpResponseRedirect('/berichten/')
        # return super().form_invalid(form)


def berichtenPage(request):
    # messages.set_level(request, messages.WARNING)
    messages.add_message(request, messages.INFO, "Welkom bij Viking Lockers.")    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    obs= Q(obsolete=True)
    qs_out=Locker.objects.all().exclude(obs).filter(verhuurd=False).order_by('topic')[0:15] #we laten 15 vrije lockers zien
    return render(request, 'base/messages1.html', {'qq':q,'onverhuurd':qs_out})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def deleteBericht(request, pk):
    message = Bericht.objects.get(id=pk)

    if request.user != message.user and not request.user.is_superuser:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('berichten')
    return render(request, 'base/delete.html', {'obj': message})


class LockerUpdate( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Locker
    form_class=LockerForm
    template_name='base/locker_form.html'
    # initial = {"key": "value"}
    print('in lockerupdate')
    success_url = reverse_lazy('home')
    
    def get_object(self):
        print('in get_object')
        _id = self.request.GET.get('pk') if self.request.GET.get('pk') != None else ''
        print(_id)
        obj = get_object_or_404(Locker, id=self.kwargs['pk'])
        return obj
    def get_form_class(self):
        if self.request.user.is_superuser:
            return LockerFormAdmin
        else:
            return LockerForm
    def get_context_data(self, **kwargs):
        print('in get_context_data')
        context = super().get_context_data(**kwargs)
        context["lockers"] = Locker.objects.all()
        # obj = super().get_object(**kwargs)
        return context
    
    def form_valid(self, form):
        print('in form_valid')
        # hoofdhuurder = form.cleaned_data['verhuurd']  
        name = form.cleaned_data['nieuwe_huurder']  
        tekst = form.cleaned_data['tekst']  
        messages.success(self.request, "The Locker was updated successfully.")
        success_url = reverse_lazy('lockers')
        return super(LockerUpdate,self).form_valid(form)

@login_required(login_url='login') #nog als voorbeeeld voor veldbijwerken bewaren
def update_locker(request,pk):
    locker = Locker.objects.get(id=pk)
    form = LockerForm(instance=locker)
    vikingers=Person.objects.all().order_by('name')
    url = "/berichten/"
    if request.user.email != locker.email and not request.user.is_superuser:
        messages.add_message(request,messages.INFO, f'{locker.kluisnummer} : Is niet uw locker')
        if locker.opgezegd ==True: # and not request.user.is_superuser:
            opgezegd = formats.date_format(locker.opzegdatum, "SHORT_DATE_FORMAT")
            messages.add_message(request,messages.INFO, f'{locker.kluisnummer} : Huur is opgezegd! per {opgezegd}')
        return HttpResponseRedirect(url)
        # return HttpResponseRedirect(url)
    else:
        url = reverse('update-locker2', kwargs={'pk':locker.id})
        return HttpResponseRedirect(url)
# ---------------------------------------------------------------------------    
class LockerListView(ListView,FormView):
    model=Locker
    # template_name='home.html'
    template_name='base/lockerview_list.html'
    form_class=FormatForm
    context_object_name = "locker_list"

    def get_queryset(self) :
        queryset=Locker.objects.all().filter(verhuurd=True).order_by('locker')
        return queryset
    
    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        print('in lockerlistview get_context_data:',q)
        s='base_locker';l=len(s)+1
        verh=Q(locker__icontains=q)
        headers=Locker.objects.all().query.get_meta().fields 
        fields=['id','kluisnummer','email','tekst','verhuurd','opgezegd','updated','code']
        header=[]
        for k in headers:
            if str(k)[l:] in fields:
                header.append(str(k)[l:])              

        obs= Q(obsolete=True)
        context = super().get_context_data(**kwargs)
        qs_in=Locker.objects.all().filter(verhuurd=True).order_by('locker')
        qs_out=Locker.objects.all().exclude(obs).filter(verhuurd=False).order_by('locker')
        if 'verhuurd' in q and q:
            verh= Q(verhuurd=True)
        qs_in =Locker.objects.exclude(obs).filter(
        (Q(kluisnummer__icontains=q) |
        Q(vorige_huurder__icontains=q)|
        Q(nieuwe_huurder__icontains=q)|
        Q(email__icontains=q)|
        Q(code__contains=q)|
        Q(tekst__icontains=q)| verh )
        ).order_by('locker')
        if q:qs_out=None
        if not q: qs_in = self.get_queryset()
        context["lockers_in"] = qs_in
        context["lockers_out"] =qs_out
        self.object_list = qs_in
        context["header"] = header
        context["table"] = s
        return context

    def post(self,request,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        qs_in =Locker.objects.filter(
        Q(kluisnummer__icontains=q) |
        Q(email__icontains=q)|
        Q(tekst__icontains=q)&
        Q(verhuurd=True)
        ).order_by('locker')
        if not q:
            qs = self.get_queryset()
            qs=Locker.objects.all().filter(verhuurd=True).order_by('locker')

        else:
            qs=qs_in
        data_set=LockeradminResource().export(qs)
        format=request.POST.get('format')
        if format=='xls': ds=data_set.xls
        elif format=='csv': ds=data_set.csv
        else: 
            ds=data_set.json
        response=HttpResponse(ds,content_type=f"{format}")
        response['Content-Disposition'] = f"attachment;filename=lockers.{format}"
        return response
# ---------------------------------------------------------------------------
def lockersPage2(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    kluisjes=Locker.objects.all().filter(verhuurd=True)     
    allekluisjes=Locker.objects.all()     
    lijst='verhuurd'
    print('lockers:',q)
    A=Q(email__icontains=q)
    topics=Topic.objects.all()
    verhuurd =Locker.objects.filter(
    Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q) 
    ).order_by('locker')# .exclude(id__in=onverhuurd_lijst)

    context = {
                'verhuurd': verhuurd,
                    'lijst': lijst,
                'kluisjes': kluisjes,
                'allekluisjes': allekluisjes,
                'topics': topics,
            }
    return render(request, 'base/kluisjes.html', context)
    # return render(request, 'base/kluisjes.html', {'lockers': lockers})

def tools(request):
        # emptypersonfile=request.POST.get('personfile')
        url='tools'
        context = {
    }
        return render(request, 'base/tools.html', context)

def all_entrantsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print('entrants:',q)
    entrants_in =Locker.objects.filter(
    (Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q)|
    Q(locker__icontains=q)) & Q(verhuurd=True)
    ).order_by('locker')# .exclude(id__in=onverhuurd_lijst)

    isin = (Locker.objects
        .values('email')
        .annotate(aantal=Count('id'))
        .order_by()
        )   
    print('isin',isin.count())
    doubles = (Locker.objects
        .values('kluisnummer')
        .annotate(dcount=Count('id'))
        .order_by()
        )   
    for d in isin:
        if d['aantal'] >1:
            print(d,d['aantal'])
            messages.add_message(request, messages.INFO, f"{d}")    

    headers=Locker.objects.all().query.get_meta().fields 
    header=[]
    fields=['kluisnummer','email',]
    u=[]
    kols=[]
    s='base_locker';l=len(s)+1
    headers=Locker.objects.all().query.get_meta().fields 
    header=[]
    for k in headers:
        if str(k)[l:] in fields:
            kols.append(str(k)[l:])              
    if request.method =="POST":
        verhuurd=request.POST.get('isin')
#  ----------------------------------------------------------
        if verhuurd:
            e=Locker.objects.all().filter(id=verhuurd).first()
            if  e.verhuurd==False:
                e.verhuurd=True
                e.save()
        print('in',verhuurd)
        is_out=request.POST.get('isout')
#  ----------------------------------------------------------
        if is_out:
            e=Locker.objects.all().filter(id=is_out).first()
            if  e.verhuurd==True:
                e.verhuurd=False
                # e.save()
        print('out',is_out)
    # entrants_in= Locker.objects.filter(verhuurd = True)
    # entrants_out= Locker.objects.filter(verhuurd = False)


    # entrants_in= Locker.objects.all().filter(verhuurd=True)
    # entrants_out= Locker.objects.all().filter(verhuurd=False)
    entrants_out =Locker.objects.filter(
    (Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q)|
    Q(locker__icontains=q)) & Q(verhuurd=False)
    ).order_by('locker')# .exclude(id__in=onverhuurd_lijst)

    context = {
    'entrants_in':entrants_in,
    'entrants_out':entrants_out,
    'kols': kols,
    'header': header,
    }
    return render(request, 'base/entrants.html', context)

def huuropzeggen(request, pk):
    locker = get_object_or_404(Locker, id=pk)
    now = timezone.now()
    try:
        selected_choice = request.GET.get('opgezegd') if request.GET.get('opgezegd') != None else ''
    except (KeyError, Locker.DoesNotExist):
        # Redisplay the form.
        return render(request, 'base/locker_form.html', {
            'locker': locker,
            'error_message': "You didn't select a choice.",
        })
    else:
        print(selected_choice)
        if request.method == 'POST':
            locker.opgezegd=True
            locker.verhuurd=False
            locker.opzegdatum=now #date.datetime.now()
            locker.save()
            return redirect('home')
        return render(request, 'base/delete.html', {'obj': locker})
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('update-locker', args=(locker.id,)))
            
def lockersPage3(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    kluisjes=Locker.objects.all().filter(verhuurd=False)     
    allekluisjes=Locker.objects.all()     
    A=Q(email__icontains='vrij')
    B=Q(email__icontains='bekend')
    C=Q(obsolete=True)
    D=Q(opgezegd=True)
    E=Q(email__icontains='--')
    F=Q(email__icontains='==')
    onverhuurd =Locker.objects.all().filter( A | B |  C | D | E | F ).order_by('topic')
    lijst='onverhuurd'
    context = {
                'onverhuurd': onverhuurd,
                    'lijst': lijst,
                'kluisjes': kluisjes,
                'allekluisjes': allekluisjes,
            }
    return render(request, 'base/kluisjes.html', context)

def decodeer(regel,de_matriks_kolom,column,cellengte):
    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def resetsequence(*args):        
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM sqlite_sequence");
    results = namedtuplefetchall(cursor)
    # print(args[0])
    tabel=args[0]
    sql="UPDATE sqlite_sequence SET seq =0 where name='" + tabel + "'"
    cursor.execute(sql)
