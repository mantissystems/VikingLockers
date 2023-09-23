import csv
from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
# from viking.models import  Matriks,KluisjesRV
from base.models import Room,Message,User,Topic,Locker,Ploeg,Helptekst,Bericht,Excellijst,Person,Facturatielijst
from django.db.models import Q
from base.forms import RoomForm, UserForm,  MyUserCreationForm,PloegForm,LockerForm,ExcelForm,PersonForm,WachtlijstForm
from django.views.generic import(TemplateView,ListView)
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.db import connection
from collections import namedtuple
from rest_framework import status
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.http import JsonResponse
# from django.core.mail import send_mail
from django.core import mail
# from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
# from base.serializers import UserSerializer, UserSerializerWithToken


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
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # email_used=bool
    form = MyUserCreationForm()
    pemail=request.POST.get('email')
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if not form.is_valid():
            post_email = form.cleaned_data.get('email') # Extracting the email value from the form
            if User.objects.filter(email=post_email).exists():
                print('invalid')
            messages.error(request, f'[Email]  and/or [Username] already in use.')

        if form.is_valid():
            print('valid')
            user = form.save(commit=False)
            # user.username = user.name.lower()
            # user.last_name = user.name.lower()
            users =User.objects.filter(
            Q(username=request.POST.get('name')) |
            Q(email=request.POST.get('email'))
            ).order_by('username') #.exclude(verhuurd=False)
            print(users)
            if users:
            #     messages.error(request, 'Invalid form submission.')
            #     messages.error(request, form.errors)
            #     messages.error(request, f'[Email]  and/or [Username] already in use.')
                print('double', users)
            #     return HttpResponseRedirect('/')
            else:
                print('single',request.POST.get('name'),request.POST.get('email'))
                user.save()
                login(request, user)
                return redirect('/')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    lijst='home'
    from django.utils.safestring import mark_safe
    messages.add_message(request, messages.INFO, "Welkom bij Viking Lockers.")    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    qq=q.lower()
    # lockers=Locker.objects.all().filter(verhuurd=True)     
    messagelocker=Locker.objects.all().first()     
    from django.db.models import Count
    if request.method == 'POST':
            message = Bericht.objects.create(
            user=request.user,
            locker=messagelocker,
            body=request.POST.get('body')
        )
    if request.user.is_authenticated:
        try:
            user=User.objects.get(id=request.user.id)
            locker2 = Locker.objects.get(kluisnummer=user.locker,email=user.email,verhuurd=True)
            if locker2:
                messages.info(request, mark_safe(f"Beheer uw locker: <a href='{locker2.id}/update-locker'>{locker2.kluisnummer}</a>"))
            else:
                messages.info(request, f'U heeft nog geen  locker.')
        except:
            print('8.not-found-user.locker:', request.user)
            pass
    elif request.user is not None:
        messages.info(request, f'Ubent niet ingelogd. Svp Inloggen / Registreren')
        print('2.not-none-user:', request.user)
        # return HttpResponseRedirect('/registreer/')
        return HttpResponseRedirect('/login/')
    elif request.user == AnonymousUser:
          print('3.anonymoususer:', request.user)
    elif request.user != AnonymousUser:
            print('4.not-none-and-not-anonymous user:', request.user)
            try:
                    user=User.objects.get(id=request.user.id)
                    yourlocker=Locker.objects.filter(email__icontains=user.email)
                    yourlocker=Locker.objects.filter(kluisnummer__icontains=user.locker)
                    cnt=yourlocker.count()
                    print('6.logged-in-user:', request.user)
            except:
                print('7.not-foundlocker-user:', request.user)
                pass
            else:
                print('7.use-user:', request.user)
    berichten=Bericht.objects.all() ##.filter(user=request.user.id)
    url = reverse('berichten',)
    if q!='' or q !=None:
        lijst='home'
        # lockers=Locker.objects.all().filter(verhuurd=True)     

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
        if 'fact' in qq:
            x = qq.replace("fact ", "")
            q=x
            url = "facturatielijst" + "?q=" +q 
            return HttpResponseRedirect(url)
        if 'pers' in qq:
            x = qq.replace("pers ", "")
            q=x
            url = "profiles" + "?q=" +q 
            return HttpResponseRedirect(url)
        if 'req' in qq:
            x = qq.replace("req ", "")
            q=x
            url = "berichten" + "?q=" +q 
            return HttpResponseRedirect(url)
        if 'usr' in qq:
            x = qq.replace("usr ", "")
            q=x
            url = "users" + "?q=" +q 
            return HttpResponseRedirect(url)

    else:
        berichten=Bericht.objects.all()
    lockers =Locker.objects.filter(
        Q(kluisnummer__icontains=q) |
        Q(email__icontains=q)
        ).order_by('kluisnummer') #.exclude(verhuurd=False)

    room_messages = Message.objects.all()
    # facturatielijst=Facturatielijst.objects.all()
    context = {
               'lijst':lijst,
                'lockers': lockers,
                # 'facturatielijst': facturatielijst,
               'berichten': berichten, 
               'room_messages': room_messages
               }
    return render(request, 'base/home.html', context)


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
    ).order_by('kluisnummer')
    return queryset
paginate_by = 10
def get_context_data(self, **kwargs):
        # return context
        context = super(LockerView, self).get_context_data(**kwargs)
        # context['pk'] = self.object.id
        # context['object_list'] = Locker.objects.all().filter(verhuurd=True)
        # print(onderhuurder)
        # vikingers=Person.objects.all().order_by('email').filter(onderhuur=True)
        # context['form'].fields['subcategory'].choices = SubcategoryFilter[self.object.type]

        # Return context to be used in form view
        return context


 
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def helpPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    aantalusers=User.objects.all()
    from django.db.models import Count
    results = (User.objects
    .values('owners')
    .annotate(dcount=Count('email'))
    .order_by()
    )   
    # results = (Locker.objects
    # .values('kluisnummer')
    # .annotate(dcount=Count('kluisnummer'))
    # .order_by()
    # )   
    # joiner=Locker.objects.none
    # cnt=0
    # joincnt=0
    # results = (Locker.objects
    # .values('kluisnummer')
    # .annotate(dcount=Count('kluisnummer'))
    # .order_by()
    # )       

    helptekst=Helptekst.objects.filter(
            #    'results': results,
            # Q(publish=True)
            Q(title__icontains=q)|
            Q(content__icontains=q)
        ).order_by('seq').exclude(publish=False)
    return render(request, 'base/helptekst.html', {'helptekst': helptekst,'aantalusers':aantalusers,'results': results,})


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
def room(request, pk):
    room = Locker.objects.get(id=pk)
    # room_messages = room.message_set.all()
    # participants = room.participants.all()
    ploegen=Ploeg.objects.all()
    vikingers=User.objects.all().order_by('email')
    topic=room.kluisnummer

    ftopic=Q(topic__icontains=topic)
    fverhuurd=Q(verhuurd=True)

    verhuurd=Locker.objects.all().filter(ftopic&fverhuurd)  #verzamel verhuurde kluisjes voor de room 

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    # heren=Matriks.objects.filter(naam__icontains=topic).exclude(y_as__in=(7,8,9)).order_by('y_as')
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    for i in range (0,9):
        kopmtrx.append(hdr[i])
    if topic=='Wachtlijst':
        hdr=['wachtlijst']
        kopmtrx=hdr
    topics = Topic.objects.all()[0:5]
    # q='H35'  #temporary value to test 'highlight' templatetag
    q=' '
    context = {
        'room': room,
               'topics': topics,
                # 'heren': heren,
                'ploegen': ploegen,
                'verhuurd': verhuurd,
                'kopmtrx': kopmtrx,
            #    'participants': participants,
               'q':q,
            #    'room_messages': room_messages
               }

    return render(request, 'base/room.html', context)


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
        # locker = form.cleaned_data['locker']  
        # email = form.cleaned_data['email'] 
        # if locker:
        #     Locker.objects.update_or_create(kluisnummer=locker,
        #                                                    email=email,
        #                                                    verhuurd=True,
        #                                                    )
            # print(locker)
        return super(CreateUser,self).form_valid(form)

class updateUser3(LoginRequiredMixin,UpdateView):
    login_url='login'
    model = User
    # fields='__all__'
    fields = ['username','email','locker']
    success_url = reverse_lazy('users')
    def get_object(self):
        # obj = get_object_or_404(Locker, kluisnummer__slug=self.kwargs['pk'], slug=self.kwargs['pk'] )
        obj = get_object_or_404(User, id=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        kluis = form.cleaned_data['locker']  
        email = form.cleaned_data['email'] 
        name=email.split('@')
        print(name)
        if kluis:
            print(kluis)
            locker, created = Locker.objects.update_or_create(
            kluisnummer=kluis,
            email=email,
            verhuurd=True,
            type='H',
            kluisje=kluis,
            )

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
            locker, created = Locker.objects.update_or_create(
            kluisnummer=kluis,
            email=email,
            verhuurd=False,
            kluisje=kluis,
            )
        else:
                    messages.success(self.request, "Something went wrong.")
        messages.success(self.request, "The user was updated successfully.")
        return super(updateUser_email,self).form_valid(form)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    lockers = Locker.objects.all()
    member_lockers = Locker.objects.all().exclude(owners=None)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics,'lockers':lockers,'member_lockers':member_lockers}
    return render(request, 'base/profile.html', context)

# @login_required(login_url='login')
# def updatePerson(request,pk):
#     person = Person.objects.get(id=pk)
#     form = PersonForm(instance=person)
#     locker= request.POST.get('locker')
#     huur= request.POST.get('hoofhuurder')
#     wacht= request.POST.get('wachtlijst')
#     onder= request.POST.get('onderhuur')
#     email= request.POST.get('email')
#     context = {
#                 'form': form,
#                 'locker': locker,
#             }
#     if request.method == 'POST':
#         if form.is_valid():
#             print('valid')

#         if not form.is_valid():
#             print('invalid')
#             return redirect('update-person', pk=person.id)
#     return render(request, 'base/update-person.html', context)

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

def lockersPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lockers = Locker.objects.filter(kluisnummer__icontains=q,verhuurd=True) #[0:15]
    return render(request, 'base/lockers.html', {'lockers': lockers})
def vrijelockersPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lijst='vrijelockerslijst'
    # vergelijk facturatielijst van heden met de oude excellijst; ===> in_excel; waarde=lockernummer
    # vergelijk facturatielijst van heden met de registraties; ===> is_registered; waarde=lockernummer
    # lockers = Facturatielijst.objects.all() ##.filter(excel__icontains='--')
    lockers = Facturatielijst.objects.filter(
                    Q(kluisnummer__icontains='--')
                    # Q(is_registered__icontains='regis')
                    # Q(is_registered=None) #.filter(type='vrij')
                ).order_by('kluisnummer') ##.exclude(kluisnummer__icontains='--') ##.update(verhuurd=False)

    return render(request, 'base/excellijst.html', {'lockers': lockers,'vrijelockerslijst':lijst})

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
    # return render(request, 'base/delete.html', {'obj': room})
    return render(request, 'base/delete.html', {'lockers': lockers,'excellijst':lijst,'menuoptie':menuoptie})

def profilePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # profiles = User.objects.filter(name__icontains=q)
    profiles = Person.objects.all() #filter(name__icontains=q)
    return render(request, 'base/profiles.html', {'profiles': profiles})

def ploegPage(request, pk):
    ploeg = Ploeg.objects.get(name=pk)
    participants = ploeg.participants.all()
    ploegen = Ploeg.objects.all()
    vikingers=User.objects.all().order_by('username')
    form = PloegForm(instance=ploeg)
    context = {
                'vikingers':vikingers,
                'participants': participants,
                'ploegen':ploegen,
                'ploeg': ploeg,
                'form': form,
            }
    if request.user.ploeg != ploeg.name:
        messages.error(request, f"'{ploeg.name}' : Is niet uw ploeg")
        return render(request, 'base/ploegen.html', context)

    if request.method == 'POST':
        form = PloegForm(request.POST, request.FILES, instance=ploeg)
        teamlid= request.POST.get('teamlid')
        teamlideraf= request.POST.get('teamlideraf')
        if form.is_valid():
            print('form is valid')
            if teamlid:
                t=User.objects.get(id=teamlid)
                ploeg.participants.add(t)
            if teamlideraf:
                t=User.objects.get(id=teamlideraf)
                ploeg.participants.remove(t)
            form.save()
            # return redirect('ploegen')
            return redirect('ploeg', ploeg.name)

    return render(request, 'base/update-ploeg.html', context) ##{'form': form})

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
    
    # if request.user.email != locker.email and not request.user.is_superuser:
    #     messages.error(request, f'{locker.kluisnummer} : Is niet uw locker')
    #     return render(request, 'base/berichten.html', {'lockers': lockers,'topics':topics})
    
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
            # if kluis:
            #     created = Locker.objects.update_or_create(kluisnummer=kluis.id,
            #         email=excel.email,
            #         verhuurd=True,
            #         kluisje=kluis.id)

            if onderhuurder:
                print('onderhuurder', onderhuurder)
                h=User.objects.get(id=onderhuurder)
                # excel.owners.add(h)
                return redirect('locker', kluis.id)
            if huuropheffen:

                h=User.objects.get(id=huuropheffen)
                print('opheffen',h)
                # locker.owners.remove(h)
                form.save()
            return redirect('excel-regel', kluis.id)
    return render(request, 'base/excellijst_form.html', context)
    # return render(request, 'base/update-locker.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # if request.user != room.host:
    #     return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

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
        queryset = Person.objects.filter(
            Q(email__icontains=query)|
            Q(name__icontains=query)|
            Q(locker__icontains=query)
            ).order_by('email')
        context = {
            'query': query,
            'object_list' :queryset,
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
    model=Facturatielijst
    def get_context_data(self,**kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') != None else ''
        query = self.request.GET.get('q')
        print(query)
        if query == None: query=""
        queryset = Facturatielijst.objects.all().filter(
            Q(email__icontains=query)|
            Q(kluisnummer__icontains=query)|
            Q(in_excel__icontains='==')&Q(is_registered__icontains='==')
            ).order_by('kluisnummer')
        context = {
            'query': query,
            'object_list' :queryset,
            }
        return context


class PersonUpdate_id( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Person
    # fields = ['name','email','verhuurd','sleutels','code','kluisje']

    # fields = ['name','email','wachtlijst']
    fields = '__all__'
    success_url = reverse_lazy('profiles')
    def form_valid(self, form):
        kluis = form.cleaned_data['locker']  
        onderhuur = form.cleaned_data['onderhuur']  
        print(onderhuur)
        email = form.cleaned_data['email']
        hoofdhuurder = form.cleaned_data['hoofdhuurder']  
        name = form.cleaned_data['name']  
        onderhuurder = form.cleaned_data['onderhuur']  
        wachtlijst = form.cleaned_data['wachtlijst']  
        email = form.cleaned_data['email'] 
        tekst = form.cleaned_data['tekst']  
        # print(tekst)
        if wachtlijst:            
            if tekst:
                if ';' in tekst and '@' in email:
                    txt=tekst.splitlines()
                    for t in txt:
                        print(t)
                        u=t.replace(';','')
                        user=Person.objects.update_or_create(name=t,
                                                           email= t + '@viking.nl',
                                                           locker=kluis,
                                                           wachtlijst=True,
                                                           )
        # url = reverse('delete-person', kwargs={'pk': super().person.id})
        viking= email.replace("@", "")
        print(viking)
        string='pbkdf2_sha256$390000$MbAy3r2ahV6QE6xFilyWG5$Hkuz0s9MNtjJ066lD0v9N2tnUv2ZuZLALt2rIL1QSAQ='
 
        if onderhuur==True:
            try:
                u=User.objects.get(email=email)
            except:
                user,User.objects.update_or_create(username=email,
                                                           email=email,
                                                           is_active=True,
                                                           first_name=name,
                                                           last_name=name,
                                                           password=string,
                                                           )
                print('onderhuurder')

        return super(PersonUpdate_id,self).form_valid(form)
        messages.success(self.request, "The person was updated successfully.")

class EditFactuur( LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    model = Facturatielijst
    fields = ['kluisnummer','email','in_excel','is_registered','type']
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

@login_required(login_url='login')   
def tel_aantal_registraties(request):
    print('in tel_aantal_registraties in facturatielijst===============')
    # qs_user = User.objects.all()[0:1]
    # locker= Locker.objects.none()
    # qs1=qs_user.values_list('email',flat=True)
    # qs_locker = Locker.objects.all()
    # qs_excel = Excellijst.objects.all()
# begin eenmalig dd20-09-23
    # onderhuurders = User.objects.filter(
    #         Q(email__icontains='mantis')
    #         ).exclude(email__icontains='wej')
    # for p in onderhuurders:
    #     x = p.email.replace("mantis", "viking")
    #     print(x)
    #     p.email=x
    #     p.save()
# einde eenmalig dd20-09-23
    # print('bestaat factuur als locker ===============')
    # for f in Facturatielijst.objects.all():
    #     if Locker.objects.all().filter(kluisnummer=f.kluisnummer).exists():
    #         l=Locker.objects.all().filter(kluisnummer=f.kluisnummer).update(sleutels=8)

    #         # try:
    #         #     Locker.objects.get(kluisnummer=f.kluisnummer)
    #         #     print(f.kluisnummer,'heeft WEL factuur')
    #         # except: Locker.DoesNotExist
    #         print(f.kluisnummer,'heeft GEEN factuur')
            # f=Facturatielijst.objects.all().filter(email=u.email).update(type='X')

    print('in tel_aantal_users in facturatielijst===============')
    # for u in qs_user:
    #     if Facturatielijst.objects.all().filter(email=u.email).exists():
            # f=Facturatielijst.objects.all().filter(email=u.email).update(is_registered='==regis==',in_excel=u.id)
            # try:
            #     User.objects.get(email=u.email)
            # except: User.DoesNotExist
            # print(u.email,'X')
            # f=Facturatielijst.objects.all().filter(email=u.email).update(type='X')
    print('in tel_aantal_lockers in facturatielijst===============')
    kluisjes = Locker.objects.all()
    # kluisjes = Locker.objects.filter(
        # Q(kluisnummer__icontains='heren')&
        # Q(verhuurd=True)
        # )

    for k in kluisjes:
        if Facturatielijst.objects.all().filter(kluisnummer=k.kluisnummer).exists():
            locs= Facturatielijst.objects.all().filter(kluisnummer=k.kluisnummer)
            # if locs.count() <=1:
            try:
                Facturatielijst.objects.get(kluisnummer=k.kluisnummer)
            except Facturatielijst.DoesNotExist:
                print(k.kluisnummer,'locker niet in facturatielijst','toegevoegd')
                Facturatielijst.objects.update_or_create(
                email='vrij',
                in_excel='nakijken', 
                kluisnummer=k.kluisnummer
                )

        else:
                print(k.kluisnummer,'locker niet in facturatielijst','toegevoegd')
                Facturatielijst.objects.update_or_create(
                email='vrij',
                in_excel='nakijken', 
                kluisnummer=k.kluisnummer
                )
    # # ===begin eenmalige create vanuit excellijst
    # print(l.kluisnummer,'=>bestaat excel locker in locker?')

    # for loc in Excellijst.objects.all():
    #     if Facturatielijst.objects.all().filter(email=loc.email).exists():
    #         if Facturatielijst.objects.all().count()<1:
    #             try:
    #                 Facturatielijst.objects.get(email=loc.email)
    #             except Facturatielijst.DoesNotExist:
    #                 Facturatielijst.objects.update_or_create(
    #                 email=loc.email,
    #                 kluisnummer=loc.kluisnummer
    #             )
    #             print(loc.kluisnummer,'=>in facturatielijst')
    # ===einde eenmalige create vanuit excellijst
    verhuurd = Locker.objects.filter(
        # Q(kluisnummer__icontains='heren')&
        Q(verhuurd=True)
    )
    print('komt verhuurde locker voor in excellijst ======')
    # for v in verhuurd:
    #     if Excellijst.objects.all().filter(kluisnummer=v.kluisnummer).exists():
    #         print(v.kluisnummer,' zit in excellijst')
    #     else:
    #         print(v.kluisnummer,v.email,' zit niet in excellijst')
    # print('is excellijst een verhuurde locker ======')
    # x=0
    # qs_excel = Excellijst.objects.filter(
    #     Q(kluisnummer__icontains='dames')
    #     # Q(kluisnummer__icontains='heren')
    # )

    # for qs in qs_excel:
    #     if Locker.objects.all().filter(kluisnummer=qs.kluisnummer).exists():
    #         print(qs.kluisnummer,' is verhuurd')
    #     else:
    #         x+=1
    #         print(x,qs.kluisnummer,qs.email,' heeft nog geen locker')
    #     # if not Locker.objects.all().filter(kluisnummer=loc.kluisnummer).exists():
    #         # if Locker.objects.all().count()<1:
    #             # try:
    #             #     Locker.objects.get(email=loc.email)
    #             # except Locker.DoesNotExist:
    #         # if 'Heren' in loc.kluisnummer:
    #         #     print(loc.kluisnummer)
    #         #     create,cre=Locker.objects.update_or_create(
    #         #                 kluisnummer=loc.kluisnummer,
    #         #                 kluisje=loc.kluisnummer,
    #         #                 topic='----',
    #         #                 email='onbekend@viking.nl',
    #         #                 verhuurd=False,
    #         #                 code=0,
    #         #                 sleutels=0
    #         #                 ) 
    #     #     create.owners.add(request.user) 
    #         # ### one at a time by the position of break
    #             # break

    # print(qs_user.count(),qs_locker.count(),qs_excel.count())
    print('einde tel_aantal_lockers in facturatielijst')
    url = reverse('excellijst',)
    return HttpResponseRedirect(url)

# def export_search_csv(request, start_date, end_date):
def export_search_csv(request,):
    import csv
    # filename="facturatie_lijst.csv"'
    # spamreader = csv.reader(filename, delimiter=' ', quotechar='|')
    # for row in spamreader:
        # print(', '.join(row))
        # Spam, Spam, Spam, Spam, Spam, Baked Beans
        # Spam, Lovely Spam, Wonderful Spam
    data = Facturatielijst.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="facturatie_lijst.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'locker', 'email', 'type'])
    for item in data:
        writer.writerow([item.id ,item.kluisnummer, item.email, item.type,";"])
    return response

def file_load_view(request):
#         send_mail(
#     "Subject here",
#     "Here is the message.",
#     "from@example.com",
#     ["to@example.com"],
#     fail_silently=False,
# )
        # ============================================================ example write file with appropriate separators
    # header = ['name', 'area', 'country_code2', 'country_code3']
    # data = [
    # ['Albania', 28748, 'AL', 'ALB'],
    # ['Algeria', 2381741, 'DZ', 'DZA'],
    # ['American Samoa', 199, 'AS', 'ASM'],
    # ['Andorra', 468, 'AD', 'AND'],
    # ['Angola', 1246700, 'AO', 'AGO']]
    # with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
    #     writer = csv.writer(f)
    # # write the header
    #     writer.writerow(header)
    # # write multiple rows
    #     writer.writerows(data)
    # ============================================================ temporarely  commented out 13-9-23 
    # Create the HttpResponse object with the appropriate CSV header. 
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="facturatielijst.csv"'
    # # excel: 20200830VolwassenLedenPloegmakelaar.xlsx (libreoffice calc)
    # writer = csv.writer(response)
    # writer.writerow(['huurder', 'locker', 'regis', ])
    # tekst=Facturatielijst.objects.all().values_list('email','kluisnummer','is_registered')
    # # print(tekst)
    # for e in tekst:
    #     writer.writerow([e])

    # return response
    # ============================================================ temporarely  commented out 13-9-23

    # context={}
    # return render(request, 'base/home.html', context)
    # url = reverse('create_locker', kwargs={'row': pk,'kol': kol})
        url = reverse('facturatielijst',)
        return HttpResponseRedirect(url)


def lockerPage(request,pk):
    locker = Locker.objects.get(id=pk)
    form = LockerForm(instance=locker)
    lockers=Locker.objects.all().filter(verhuurd=True)
    topics=Topic.objects.all()
    vikingers=User.objects.all().order_by('username')
    context = {
                'vikingers':vikingers,
                'kluis': locker,
                'form': form,
            }
    
    if request.user.email != locker.email and not request.user.is_superuser:
        messages.error(request, f'{locker.kluisnummer} : Is niet uw locker')
        return render(request, 'base/berichten.html', {'lockers': lockers,'topics':topics})
    
    if request.method == 'POST':
        form = LockerForm(request.POST, request.FILES, instance=locker)
        onderhuurder= request.POST.get('onderhuurder')
        slotcode= request.POST.get('code')
        type= request.POST.get('type')
        sleutels= request.POST.get('sleutels')
        huuropheffen= request.POST.get('huuropheffen')
        print('onderhuurder', onderhuurder,sleutels,slotcode)
        if form.is_valid():
            print('form is valid')
            if onderhuurder:
                print('onderhuurder', onderhuurder)
                h=User.objects.get(id=onderhuurder)
                locker.owners.add(h)
                return redirect('lockers')
            if huuropheffen:

                h=User.objects.get(id=huuropheffen)
                print('opheffen',h)
                locker.owners.remove(h)
                form.save()
            return redirect('locker', locker.id)
    return render(request, 'base/update-locker.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    # if request.user != room.host:
    #     return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


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
    return render(request, 'base/room_form.html', context)

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
    success_url = reverse_lazy('excellijst')
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
    fields = ['name','email','tekst']
    success_url = reverse_lazy('home')

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if request.user.is_superuser:
            fields.append('tekst')
        return fields
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('personmail') if self.request.GET.get('personmail') != None else ''
        query = self.request.GET.get('personmail')
        if query == None: query=""
        print(query)
    #     queryset = Person.objects.
    #     context = {
    #         'query': query,
    #         'object_list' :queryset,
    #         }
        # user = self.request.user
        context["email"] = query #user.ticket_set.all()
        return context

    #     return context
    
    def form_valid(self, form):
        messages.success(self.request, "U bent op de wachtlijst geplaatst.")
        return super(CreatePerson,self).form_valid(form)

def berichtenPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q!='' or q !=None:
        berichten = Bericht.objects.filter(body__icontains=q)
    else:
        berichten = Bericht.objects.all()
    messagelocker=Locker.objects.all().first()     
    if request.method == 'POST':
        message = Bericht.objects.create(
        user=request.user,
        locker=messagelocker,
        body=request.POST.get('body')
        )
    print(q)

    return render(request, 'base/berichten.html', {'berichten': berichten})


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

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)

class LockerUpdate( LoginRequiredMixin,JsonableResponseMixin,UpdateView):
    login_url = '/login/'
    # redirect_field_name = 'redirect_to'

    model = Locker
    # fields='__all__'
    fields = ['kluisnummer','email','verhuurd','sleutels','code','kluisje','owners','type']
        # if request.user.email != locker.email and not request.user.is_superuser:
        # messages.error(request, f'{locker.kluisnummer} : Is niet uw locker')
        # return render(request, 'base/berichten.html', {'lockers': lockers,'topics':topics})

    # fields = ['name','email','wachtlijst']
    # fields = '__all__'
    success_url = reverse_lazy('lockers')
    # def get_object(self):
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            # obj=self.get_object()
    def get_context_data(self, **kwargs):
        # Load context from GET request
        SubcategoryFilter = [
            ('--', '--'),
            ('H', 'hang'),      #gebruiker heeft hangslot
            ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
            ]
        context = super(LockerUpdate, self).get_context_data(**kwargs)
        # Get id from PhysicalPart instance 
        context['pk'] = self.object.id
        # Get category from PhysicalPart instance
        context['type'] = self.object.type
        # Add choices to form 'subcategory' field
        context['form'].fields['type'].choices = SubcategoryFilter[0:]
        context['vikingers'] = Person.objects.all()
        # print(onderhuurder)
        vikingers=Person.objects.all().order_by('email').filter(onderhuur=True)
        # context['form'].fields['subcategory'].choices = SubcategoryFilter[self.object.type]

        # Return context to be used in form view
        return context

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet 
    #     context["vikingers"] = Locker.objects.all()
    #     # obj = super().get_object(**kwargs)
    #     # print(obj,'context')
    #     return context
            # if self.request.user.email != obj.email and not self.request.user.is_superuser:
            #   notyours='notyours'
            #   messages.error(self.request, f'{obj.kluisnummer} : Is niet uw locker')
            # # url = reverse('home',)
            # context={'notyours':'notyours'}
            # return context
        # return super().get_context_data(**kwargs)
    
    def get_object(self):
        obj = get_object_or_404(Locker, id=self.kwargs['pk'])

        _id = self.request.GET.get('pk') if self.request.GET.get('pk') != None else ''
        print(_id)
        try:
            obj = get_object_or_404(Locker, id=self.kwargs['pk'])
            print(obj.email,self.request.user.email)
            if self.request.user.email != obj.email and not self.request.user.is_superuser:
            #   notyours='notyours'
              messages.error(self.request, f'{obj.kluisnummer} : Is niet uw locker')
              obj=None
            # url = reverse('home',)
            # context={'notyours':'notyours'}
            # return context
        # return super().get_context_data(**kwargs)

            return obj
        except ValueError:
                obj = get_object_or_404(Locker, kluisnummer=self.kwargs['pk'])
                return obj
        # obj = get_object_or_404(User, email__slug=self.kwargs['email'], slug=self.kwargs['email'] )
        # obj = get_object_or_404(User, id=self.kwargs['pk'])
        # return obj

    def form_valid(self, form):
        kluis = form.cleaned_data['kluisnummer']  
        email = form.cleaned_data['email'] 
        return super(LockerUpdate,self).form_valid(form)
        messages.success(self.request, "The person was updated successfully.")

@login_required(login_url='login')
def update_locker(request,pk):
    locker = Locker.objects.get(id=pk)
    form = LockerForm(instance=locker)
    vikingers=User.objects.all().order_by('username')
    if request.user.email != locker.email and not request.user.is_superuser:
        messages.error(request, f'{locker.kluisnummer} : Is niet uw locker')
        url = reverse('home',)
        return HttpResponseRedirect(url)

    if request.method == 'POST':
        form = LockerForm(request.POST, request.FILES, instance=locker)
        onderhuurder= request.POST.get('onderhuurder')
        slotcode= request.POST.get('code')
        type= request.POST.get('type')
        email=request.POST.get('email')
        sleutels= request.POST.get('sleutels')
        huuropheffen= request.POST.get('huuropheffen')
        print('onderhuurder', onderhuurder,sleutels,slotcode)
        if form.is_valid():
            print('form is valid')
            if onderhuurder:
                print('onderhuurder', onderhuurder)
                h=User.objects.get(id=onderhuurder)
                locker.owners.add(h)
                return redirect('lockers')
            if huuropheffen:

                h=User.objects.get(id=huuropheffen)
                print('opheffen',h)
                locker.owners.remove(h)
                form.save()

            if locker.verhuurd == False:
                users_found=User.objects.all().values_list('email',flat=True)
                overigelockers = Locker.objects.filter(
                    Q(verhuurd=False)&
                    Q(email=request.user.email)
                ).order_by('kluisnummer').update(verhuurd=False)
                try:
                    locker2 = Locker.objects.get(kluisnummer=locker.kluisnummer,email=locker.email)
                except Locker.DoesNotExist:
                    print( 'except verhuurd of niet',locker.kluisnummer,locker.verhuurd)
            if locker.verhuurd == True:
                locker.email=email           
                overigelockers = Locker.objects.filter(
                    Q(verhuurd=False)&
                    Q(email=locker.email)
                ).order_by('kluisnummer')
            form.save()
            # return redirect('home')

    return render(request, 'base/update-locker.html', {'form': form,'vikingers':vikingers,'kluis':locker})

# @login_required(login_url='login')
# def update_kluis(request, pk):
    # column=int(kol)
    # matrix=Matriks.objects.get(id=pk)
    # rms = Locker.objects.all().filter(verhuurd=True)
    # owner_count=0
    # rgl=matrix.y_as
    # owners=[]    
    # hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    # dematrikskolom=hdr[column];print(dematrikskolom)
    # kluisje=getattr(matrix,dematrikskolom)
    # matriksnaam=getattr(matrix,'naam')
    # opheffen= request.POST.get('opheffen')
    # column=int(kol)
    # regel=matrix.regel
    # oorspronkelijkmatriksnummer=decodeer(regel,dematrikskolom,column,cellengte=3)
    # print('oorspronkelijkmatriksnummer',oorspronkelijkmatriksnummer)

    # try:
    #     kls=Locker.objects.get(email=opheffen)
    #     try:
    #         print(kls)
    #         # messages.error(request, f'{matriksnaam}: Geen huurders verder.')
    #         # return redirect('home')
    #     except:
    #         pass
    # except: 
    #     Locker.DoesNotExist
    #     # messages.error(request, f'{pk} {kol}: Niet gevonden')
    #     # url = reverse('create_locker', kwargs={'row': pk,'kol': kol})
    #     url = reverse('update-locker', kwargs={'pk': pk})
    #     return HttpResponseRedirect(url)
    #     # return HttpResponseRedirect('/info/')
    # if request.method == 'POST':
    #     huurder= request.POST.get('heeftkluis')
    #     label= request.POST.get('kluislabel')
    #     slot= request.POST.get('slot')
    #     sleutels= request.POST.get('sleutels')
    #     code= request.POST.get('code')
    #     print(sleutels,code)
    #     your_name= request.POST.get('your_name')
    #     huuropheffen= request.POST.get('huuropheffen')
    #     kls.userid=huurder
    #     kls.verhuurd=True
    #     # return HttpResponseRedirect('/')
    #     if slot:
    #         kls.type=slot
    #         kls.save()
    #     if huurder or your_name:
    #         h=User.objects.get(id=huurder)
    #         kls.owners.add(h)
    #         setattr(kls, 'verhuurd',True)
    #         kls.save()
    #     if huuropheffen:
    #         h=User.objects.get(id=huuropheffen)
    #         print('opheffen..',h)
    #         kls.owners.remove(h)
    #         print(kls)
    #         setattr(kls, 'email','info@viking.nl')
    #         setattr(kls, 'verhuurd',False)
    #         kls.save()
    #     if sleutels:
    #         kls.sleutels=sleutels
    #         kls.save()
    #     if code:
    #         kls.code=code
    #         kls.save()

    #     return redirect('home')

    # vikingers=User.objects.all().order_by('username')
    # context = {
    #             'vikingers':vikingers,
    #             'kluis': kls,
    #             'verhuurd': rms,
    #             # 'huurders': huurders,
    #             # 'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
    #         }
    # return render(request, 'base/update_kluis_form.html', context)


def lockersPage2(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # lockers = Locker.objects.filter(kluisnummer__icontains=q,verhuurd=True) #[0:15]
    
    lockers =Locker.objects.filter(
        Q(kluisnummer__icontains=q) |
        Q(email__icontains=q)
        ).order_by('kluisnummer') #.exclude(verhuurd=False)

    return render(request, 'base/kluisjes.html', {'lockers': lockers})

def decodeer(regel,de_matriks_kolom,column,cellengte):
    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer


class Blokken(TemplateView):
    template_name = 'base/home.html'
    def get_context_data(self, **kwargs):
        hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12',]#'kol13',] #'kol14']
        # begincell=0;cellengte=0;eindcell=0
        begincell=0;cellengte=0;eindcell=0;kolomteller=0;rij=0
        topics=Room.objects.all().exclude(name='Wachtlijst')
        kasten= topics #['Heren','Adames','Bdames','Cdames','Ddames']
        # Matriks.objects.all().delete()
        for k in kasten:
            regelteller=0
            print(k,len(hdr))
            matrixnaam=k.name 
            bloknummer='' ;   vv= matrixnaam[0:1]      #voorvoegsel
            nr=len(hdr)
            kolommen = len(hdr)-3
            ronde=len(hdr)
            r = 0
            rijen=len(hdr)
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
                        s += vv + str(r).zfill(2) #+'|.'
                        if p%2 == 0:
                            w1 += str(ronde)
                            w1 = ""
                        # else:
                        #     r+=1
                        #     s += vv + str(r).zfill(2) #+'|!'
                        #     ronde += 1

                    # if teama == teamb:
                    #     r+=1
                    #     s +=vv +  str(r).zfill(2) #+'|='
                    #     if r==len(hdr):r=0
                print(s)
        #         # ALS DE MATRIKS AL IS AANGEMAAKT,NIET MEER UITVOEREN, wordt opgenomen in het instellingen bestand
                regelteller+=1
                # Matriks.objects.update_or_create( 
                #         kop=s,
                #         regel=s,
                #         # ronde=r,
                #         # x_as=r,
                #         y_as=regelteller,
                #         naam=matrixnaam,
                #         )    
                # if regelteller==len(hdr):regelteller=0
                        
        return

def hernummermatriks(request):
    print('in hernummermatriks===============')
    # rij=0
    # matriks regel-kolomnummering naar kolomvelden overbrengen
    hdr=['','kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13','kol14']
    begincell=0;cellengte=0;eindcell=0
    # matrixen=Matriks.objects.all().values_list('naam',flat=True).distinct()
    matrixen= ['Heren','ADames','BDames','CDames','DDames']

    # from django.db.models import Count
    # results = (Matriks.objects
    # .values('naam')
    # .annotate(dcount=Count('naam'))
    # .order_by()
    # )   

    # matrix=Matriks.objects.filter(y_as__in=(1,2,3,4,5,6)).order_by('y_as').order_by('naam')
    # matrix=results
    # for r in matrixen:
    #     print(r)
        # matrix=Matriks.objects.filter(naam=r) #.first()
        # for m in matrix:
        # # m=matrix
        #     print(m)
        #     rij=str(m.y_as)
        #     cellengte=3
        #     regel=m.regel
        #     for kol in range(0,len(hdr)):
        #         de_matriks_kolom=hdr[kol]
        #         oorspronkelijkmatriksnummer=decodeer(regel,de_matriks_kolom,kol,cellengte)
        #         print(m.naam,de_matriks_kolom,begincell,oorspronkelijkmatriksnummer)
        #         setattr(m, de_matriks_kolom, oorspronkelijkmatriksnummer)
        #         m.save()
    context={}
    return render(request, 'base/home.html', context)

# def create_locker(request,row,kol):
#     hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
#     column=int(kol)
#     print('params',row,kol)
#     # matrix=Matriks.objects.get(id=row)
#     rms = Locker.objects.all()
#     # rgl=matrix.y_as
#     dematrikskolom=hdr[column];print(dematrikskolom)
#     # kluisje=getattr(matrix,dematrikskolom)
#     # matriksnaam=getattr(matrix,'naam')
#     column=int(kol)
    # regel=matrix.regel
    # oorspronkelijkmatriksnummer=decodeer(regel,dematrikskolom,column,cellengte=3)
    # print('locker:',oorspronkelijkmatriksnummer)
    # try:
        # l=Locker.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
        # regel=l.regel
    # except:
        # print('except..not found..',regel,dematrikskolom,column,oorspronkelijkmatriksnummer)
        # email=request.user.email
        # print(row,kol,'create-locker?',email)

        # if request.method == 'POST':
        #     create,cre=Locker.objects.update_or_create(
        #                     kluisnummer=oorspronkelijkmatriksnummer,
        #                     kluisje=oorspronkelijkmatriksnummer,
        #                     topic=matriksnaam,
        #                     email=email,
        #                     row=row.zfill(2),
        #                     col=kol.zfill(2),
        #                     verhuurd=True
        #                     )
        #     create.owners.add(request.user)
        #     return render(request, 'base/locker-add.html', {'column': kol,'row':row,'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer })
        #     # return redirect('home')
    # return render(request, 'base/locker-add.html', {'column': kol,'row':row,'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer })


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
