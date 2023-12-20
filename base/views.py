import csv
from typing import Any
from django import forms
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from base.models import Room,Message,User,Topic,Locker,Ploeg,Helptekst,Bericht,Excellijst,Person,Facturatielijst
from django.db.models import Q
from base.forms import RoomForm, UserForm,  MyUserCreationForm,LockerForm,ExcelForm,PersonForm,WachtlijstForm,LockerFormAdmin
from django.views.generic import(TemplateView,ListView)
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


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

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
    onverhuurd =Locker.objects.all().filter(  A | B  | C | D ).order_by('topic')
    verhuurd =Locker.objects.filter(
        (Q(verhuurd=True)
        ) 
    ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)
    # entrants_in =Locker.objects.filter(
    # Q(kluisnummer__icontains=q) |
    # Q(email__icontains=q)|
    # Q(tekst__icontains=q)|
    # Q(topic__icontains=q)&
    # Q(verhuurd=True)
    # ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)

    lockers =Locker.objects.filter(
    Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q)&
    Q(verhuurd=True)
    ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)
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
        messages.add_message(request, messages.INFO, "U bent niet ingelogd. Svp Inloggen / Registreren", extra_tags="dragonball")
        return HttpResponseRedirect(url)
    if request.user.is_authenticated:
        print('1.authorised:', request.user)
    messages.add_message(request, messages.INFO, "Welkom bij Lockermanager", extra_tags="dragonball")

    storage = messages.get_messages(request)
    # for message in storage:
        # print(message)
    # url = reverse('berichten',)
    # if q!='' or q !=None:
    #     print('if:',q)
    #     url = "lockers/"  + "?q=" +q 
    #     return HttpResponseRedirect(url)

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
    # elif 'req' in qq:
    #     x = qq.replace("req ", "")
    #     q=x
    #     url = "berichten" + "?q=" +q 
    #     return HttpResponseRedirect(url)
    elif 'usr' in qq:
        x = qq.replace("usr ", "")
        q=x
        url = "users" + "?q=" +q 
        return HttpResponseRedirect(url)

    else:
        print('else:',q)
        # if q!='' or q !=None:
        #     print('if:',q)
        url = "all_lockers/"  + "?q=" +q
        return HttpResponseRedirect(url)

class LockerView (LoginRequiredMixin,ListView):
    login_url='login'
    model=Locker
def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        context = super(LockerView, self).get_context_data(**kwargs)
        return context

def get_queryset(self): # new
    users_found=User.objects.all().values_list('email',flat=True)
    queryset = Locker.objects.filter(
        Q(verhuurd=True)&
        Q(email__in=users_found) 
    ).order_by('topic')
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
        ).order_by('topic')
    A=Q(email__icontains='vrij')
    B=Q(email__icontains='bekend')
    C=Q(obsolete=True)
    D=Q(opgezegd=True)
    E=Q(email__icontains='--')
    F=Q(email__icontains='==')
    onverhuurd =Locker.objects.all().filter( A | B |  C | D | E | F ).order_by('topic')

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
# def room(request, pk):
#     room = Locker.objects.get(id=pk)
#     ploegen=Ploeg.objects.all()
#     vikingers=User.objects.all().order_by('email')
#     topic=room.kluisnummer

#     ftopic=Q(topic__icontains=topic)
#     fverhuurd=Q(verhuurd=True)

#     verhuurd=Locker.objects.all().filter(ftopic&fverhuurd)  #verzamel verhuurde kluisjes voor de room 

#     if request.method == 'POST':
#         message = Message.objects.create(
#             user=request.user,
#             room=room,
#             body=request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room', pk=room.id)
#     # heren=Matriks.objects.filter(naam__icontains=topic).exclude(y_as__in=(7,8,9)).order_by('y_as')
#     hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
#     kopmtrx=[]
#     for i in range (0,9):
#         kopmtrx.append(hdr[i])
#     if topic=='Wachtlijst':
#         hdr=['wachtlijst']
#         kopmtrx=hdr
#     topics = Topic.objects.all()[0:5]
#     # q='H35'  #temporary value to test 'highlight' templatetag
#     q=' '
#     context = {
#         'room': room,
#                'topics': topics,
#                 # 'heren': heren,
#                 'ploegen': ploegen,
#                 'verhuurd': verhuurd,
#                 'kopmtrx': kopmtrx,
#             #    'participants': participants,
#                'q':q,
#             #    'room_messages': room_messages
#                }

#     return render(request, 'base/room.html', context)


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
            # print(user.ploeg)
            # ploeg, created = Ploeg.objects.update_or_create(name=user.ploeg)
            ploeg, created = Ploeg.objects.get_or_create(name=team)
            locker, created = Locker.objects.update_or_create(kluisnummer=user.locker,
                                                           email=user.email,
                                                           kluisje=user.locker)
            try:
                teambestaatal = Ploeg.objects.filter(name=user.ploeg)
            except: 
                Ploeg.DoesNotExist
                url = reverse('update-user')
                print('fout',user.ploeg)
                # ploeg, created = Ploeg.objects.get_or_create(name=user.ploeg)
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
    # rooms = user.room_set.all()
    lockers = Locker.objects.all()
    # member_lockers = Locker.objects.all().exclude(owners=None)
    # room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,
                # 'rooms': rooms,
               'room_messages': topics,
                 'topics': topics,
                 'lockers':lockers,
                #  'member_lockers':member_lockers
                }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def myProfile(request):
    user = request.user
    form = UserForm(instance=user)
    # print(form)
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

# @login_required(login_url='login')
# def updateRoom(request, pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)
#     topics = Topic.objects.all()
#     if request.method == 'POST':
#         topic_name = request.POST.get('topic')
#         topic, created = Topic.objects.get_or_create(name=topic_name)
#         room.name = request.POST.get('name')
#         room.topic = topic
#         room.description = request.POST.get('description')
#         room.save()
#         return redirect('home')

#     context = {'form': form, 'topics': topics, 'room': room}
#     return render(request, 'base/room_form.html', context)

# @login_required(login_url='login')   

class MemberListView (LoginRequiredMixin, ListView):
    login_url='login'
    model=User
# class MemberListView (ListView):
#     model=User
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

class PersonListView (ListView):
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

# class ExcelView (ListView):
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
        # form.fields['onderhuur'].label = "Mede Huurder"
        form.fields['tekst'].label = 'Namen  Medegebruikers'
        form.fields['wachtlijst'].label = 'Wel / Niet wachtlijst'
        # form.fields['hoofdhuurder'].label = 'Wel / Niet Hoofdhuurder'
        return form
    
    # fields=['name','tekst','wachtlijst','email','kamer']
    fields='__all__'
    success_url = reverse_lazy('wacht-lijst')
    
    def form_valid(self, form):
        kluis ='wachtlijst' ## form.cleaned_data['locker']  
        # wachtlijstaanvul = form.cleaned_data['onderhuur']  
        # print('onderhuur')
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

def export_wachtlijst(request,):
    import csv
    A=Q(kamer__in='H,D,-')
    B=Q(email__icontains='bekend')
    C=Q(wachtlijst=True)
    # D=Q(opgezegd=True)
    # E=Q(email__icontains='--')
    # F=Q(email__icontains='==')
    wachtlijst =Person.objects.all().filter( A | B |  C ).order_by('kamer','email')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="wachtlijst.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'kamer', 'email', 'wachtlijst',])
    for i in wachtlijst:
        writer.writerow([i.id ,i.kamer, i.email, i.wachtlijst ])
    return response

@login_required(login_url='login')   
def export_onverhuurd(request,):
    import csv
    A=Q(email__icontains='vrij')
    B=Q(email__icontains='bekend')
    C=Q(obsolete=True)
    D=Q(opgezegd=True)
    E=Q(email__icontains='--')
    F=Q(email__icontains='==')
    onverhuurd =Locker.objects.all().filter( A | B |  C | D | E | F ).order_by('topic')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="onverhuurd.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'tenant', 'huidig', 'oud','nieuw','keys'])
    for item in onverhuurd:
        writer.writerow([item.id ,item.email, item.kluisnummer, item.kluisje ,item.topic,item.sleutels,])
    return response

def export_emaillijst(request,):
    import csv
    # exclude_list = ['vrij', 'onbekend','wachtlijst',]
    verhuurd =Locker.objects.filter(email__icontains='@').order_by('topic')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="email_lijst.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'tenant', 'oude naam','nwe naam','huidige', 'Obs','Opg','Ver','Sl','txt','nwe','vorige'])
    for item in verhuurd:
        writer.writerow([item.id ,item.email, item.kluisje,item.topic,item.kluisnummer, item.obsolete ,item.opgezegd,item.verhuurd,item.sleutels,item.tekst,item.nieuwe_huurder,item.vorige_huurder,])
    return response
    
def export_verhuurd(request,):
    import csv
    verhuurd = Facturatielijst.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facturatie_lijst.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'tenant', 'y/n','locker','registered', 'keys','huur','obs'])
    for item in verhuurd:
        writer.writerow([item.id ,item.email, item.code,item.kluisnummer,item.is_registered, item.sleutels , item.in_excel ,item.type,item.obsolete,])
    return response


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
    messages.set_level(request, messages.WARNING)
    messages.add_message(request, messages.INFO, "Welkom bij Viking Lockers.")    
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    return render(request, 'base/messages1.html', {'qq':q,})
    # return render(request, 'base/messages1.html', {'qq':q,'locker':locker2})


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
    ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)

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
        emptypersonfile=request.POST.get('personfile')
            # Read the first line of the file
            #  ----------------------------------------------------------

#  ----------------------------------------------------------
        # ok=True
        # importfile   = open('/home/jozef/Downloads/base_person.csv', 'r')
        # sterkte=1500
        # if ok:
        #     data_set = importfile.read() #.decode('UTF-8')
        #     io_string = io.StringIO(data_set)
        #     st='I' #init
        #     for column in csv.reader(io_string, delimiter='|', quotechar="|"):
                # print(column[1])
                # if Person.objects.all().filter(name=column[1],category=column[2],rating=column[3]).exists():
                #     messages.add_message(request, messages.INFO, f"DOUBLE.not loaded->{column[1]}")    
                #     st='D' #double; alreadey loaded
                # else:
                #     st='new'
                #     try:
                #         messages.add_message(request, messages.INFO, f"loaded->{column[1]}")    
                #         column[0]*1 #must be numeric
                #         if column[2]==toernooi.category:
                #             created=Person.objects.update_or_create(
                #             id=column[0],
                #             category=column[2],
                #             rating=sterkte,
                #             name=column[1],
                #             status=st,
                #             )
                #     except:
                #         pass                        

        url='tools'
        context = {
    # 'todo':todo,
    # 'upload':upload,
    }
        # return redirect(url)    
    # print(context)

        return render(request, 'base/tools.html', context)

# def teamlideraf(request, hdr_id):
#     leden = []
#     for l in request.POST.getlist('teamlideraf'):
#         leden.append(l)
#         teamhdr = get_object_or_404(Team_hdr, id=hdr_id)
#         print(teamhdr, leden)
#     try:
#         selected_ploeg = Teamlid.objects.all().filter(id=hdr_id)
#     except (KeyError, teamhdr.DoesNotExist):
#         return render(request, 'ploeg/teamhdr_update.html', {
#             'teamhdr': teamhdr,
#             'error_message': "Selecteer een naam.", })
#     else:
#         Teamlid.objects.filter(id__in=request.POST.getlist('teamlideraf'))
#         for t in leden:
#             p = Person.objects.get(id=t)
#             # print(teamhdr, p,'teamlideraf')
#             m = Teamlid.objects.filter(ploeg=teamhdr,
#                                        member=p,)
#             m.delete()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    # return HttpResponseRedirect(reverse('ploeg:ploeg_details', args=(hdr_id,)))

def all_entrantsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    print('entrants:',q)
    entrants_in =Locker.objects.filter(
    (Q(kluisnummer__icontains=q) |
    Q(email__icontains=q)|
    Q(tekst__icontains=q)|
    Q(topic__icontains=q)) & Q(verhuurd=True)
    ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)

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
    # print('dubbelen',doubles.count())
    for d in isin:
        if d['aantal'] >1:
            print(d,d['aantal'])
            messages.add_message(request, messages.INFO, f"{d}")    
        #         k=Locker.objects.filter(name=d['kluisnummer'],topic__icontains='').last()
        #         print(k.name,k.id)
                # if k:
                    # k.delete()

    headers=Locker.objects.all().query.get_meta().fields 
    header=[]
    fields=['id','kluisnummer','email','points','kenmerk','category','opponents','verhuurd']
    u=[]
    kols=[]
    s='base_locker';l=len(s)+1
    headers=Locker.objects.all().query.get_meta().fields 
    header=[]
    for k in headers:
        if str(k)[l:] in fields:
            kols.append(str(k)[l:])              
    # kols.append('Y/N')
    # entrants_in= Locker.objects.all()
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
    Q(topic__icontains=q)) & Q(verhuurd=False)
    ).order_by('topic')# .exclude(id__in=onverhuurd_lijst)

    context = {
    'entrants_in':entrants_in,
    'entrants_out':entrants_out,
    'kols': kols,
    'header': header,
    }
    return render(request, 'base/entrants.html', context)

def polls_results(request,question_id):
    huur = get_object_or_404(Locker, id=question_id)
    context={'huur':huur.opgezegd}
    messages.add_message(request,messages.INFO, f'{huur.kluisnummer} : huur opgezegd')
    return render(request,'base/locker_form.html',context)

def polls_vote(request, question_id):
    question = get_object_or_404(Locker, id=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Locker.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/polls_detail.html', {
            'vraagje': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:polls_results', args=(question_id,)))

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
    return HttpResponseRedirect(reverse('polls_results', args=(locker.id,)))
            
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
