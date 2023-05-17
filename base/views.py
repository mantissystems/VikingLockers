from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# from viking.models import  Matriks,KluisjesRV
from base.models import Room,Message,User,Topic,Matriks,KluisjesRV
from django.db.models import Q
from base.forms import RoomForm, UserForm,  MyUserCreationForm
# Create your views here.

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
            messages.error(request, 'Username OR password does not exist')

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
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    from django.contrib.auth.models import AnonymousUser
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lockers=Matriks.objects.all()     
    from django.db.models import Count
    results = (KluisjesRV.objects
    .values('topic')
    .annotate(dcount=Count('topic'))
    .order_by()
    )   
    yourlocker=KluisjesRV.objects.none
    if request.user is not AnonymousUser:
        try:
            user=User.objects.get(id=request.user.id)
            yourlocker=KluisjesRV.objects.filter(huurders__email__icontains=user.email)
            print(yourlocker,user)
        except:
            print('except1')
            user=AnonymousUser
        try:
            yourlocker=KluisjesRV.objects.filter(email__icontains=user.email)
            print(yourlocker,user)
        except:
            print('except2')
            user=AnonymousUser

        # finally:
        # try:
        #     user=User.objects.get(id=request.user.id)
        #     yourlocker=KluisjesRV.objects.filter(huurders__email__icontains=user.email)
        #     print(yourlocker,user)
        # except:
        #     print('except')
        #     user=AnonymousUser
        # finally:
        # yourlocker=KluisjesRV.objects.filter(huurders__email__icontains=user.email)

    # if yourlocker!=None:
        # l=KluisjesRV.objects.get(id=yourlocker.id)
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
    if rooms.count()>0 and q!='':
        room_found=rooms.first()
        ftopic=Q(topic__icontains=room_found.topic)
        fverhuurdaan=Q(huurders__name__icontains=q)
        print(room_found.id)
        verhuurd=KluisjesRV.objects.all().filter(ftopic&fverhuurdaan)  #verzamel verhuurde kluisjes voor de room 
        return redirect('verhuurdaan',room_found.id, q) 
    if rooms.count()==0 and q!='':
        room_found = Room.objects.get(name='Wachtlijst')
        print('wachtlijst',room_found)
        return redirect('verhuurdaan',room_found.id, q) 
    

    context = {'rooms': rooms, 
               'topics': topics,
               'results': results,
                'lockers': lockers,
                'kopmtrx': kopmtrx,
               'room_count': room_count, 
               'yourlocker': yourlocker, 
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    vikingers=User.objects.all().order_by('email')
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
    if topic=='Wachtlijst':
        hdr=['wachtlijst']
        kopmtrx=hdr
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

def verhuurdaan(request, pk,txt):
    try:
        room = Room.objects.get(id=pk)
        print(room)
    except:
        return redirect('home') 
    finally:
        room_messages = room.message_set.all()
        participants = room.participants.all()
        vikingers=User.objects.all()
        topic=room.name
        verhuurd=KluisjesRV.objects.all().order_by('kluisnummer').filter(
            topic=topic) #.exclude(huurders=None)
        print(verhuurd.count())
            # Q(huurders__name__icontains=txt)
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
    if topic=='Wachtlijst':
        hdr=['wachtlijst']
        kopmtrx=hdr
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


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
def update_kluis(request, pk,kol):
    column=int(kol)
    matrix=Matriks.objects.get(id=pk)
    rms = KluisjesRV.objects.all()
    owner_count=0
    rgl=matrix.y_as
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    dematrikskolom=hdr[column];print(dematrikskolom)
    kluisje=getattr(matrix,dematrikskolom)
    matriksnaam=getattr(matrix,'naam')
    opheffen= request.POST.get('opheffen')
    column=int(kol)
    regel=matrix.regel
    oorspronkelijkmatriksnummer=decodeer(regel,dematrikskolom,column,cellengte=4)
    kls=KluisjesRV.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
    huurders=kls.huurders
    if huurders.count()==0: 
        messages.error(request, f'{matriksnaam}: Geen huurders verder.')
        return redirect('home')
    if request.method == 'POST':
        huurder= request.POST.get('heeftkluis')
        label= request.POST.get('kluislabel')
        slot= request.POST.get('slot')
        your_name= request.POST.get('your_name')
        huuropheffen= request.POST.get('huuropheffen')
        kls.userid=huurder
        kls.verhuurd=True

        if slot:
            kls.type=slot
            kls.save()
        if huurder or your_name:
            h=User.objects.get(id=huurder)
            kls.huurders.add(h)
            setattr(kls, 'verhuurd',True)
            kls.save()
        if huuropheffen:
            h=User.objects.get(id=huuropheffen)
            print('opheffen',h)
            kls.huurders.remove(h)
            setattr(kls, 'verhuurd',False)
            kls.save()

        return redirect('home')

    vikingers=User.objects.all().order_by('username')
    context = {
                'vikingers':vikingers,
                'kluis': kls,
                'huurders': huurders,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
    return render(request, 'base/update_kluis_form.html', context)

def kluis(request, pk):
    vikingers=User.objects.all().order_by('name')
    context={
                'vikingers':vikingers,
            }

    try:
        kls=KluisjesRV.objects.get(id=pk)
        huurders=kls.huurders.all()
        context={
                'huurders':huurders,
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
                    print('POST')
                    if huurder or your_name:
                        kls.naamvoluit=huurder
                        kluisnummer=kls.kluisnummer
                        setattr(kls, 'kluisnummer',kluisnummer)
                        kls.save()
                    if opheffen:
                        setattr(kls, 'kluisnummer', '---')
                        kls.save()
                        
            return redirect('home')

    return render(request, 'base/update_kluis_form.html', context)     

def decodeer(regel,de_matriks_kolom,column,cellengte):
    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer

def hernummermatriks(request):
    print('in hernummermatriks===============')
    # voor iedere cel in de Matriks per Room een kluisjesRV aanmaken ==================
    hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12',]#'kol13',] #'kol14']
    begincell=0;cellengte=0;eindcell=0
    topics=Room.objects.all()
    for t in topics:
        matrix=Matriks.objects.filter(naam__icontains=t.name).exclude(y_as__in=(7,8,1,2,3,4,5,6)).order_by('y_as') #matriks bevat ingeladen data 1-8 tijdens testen
        kolomteller=0
        rij=0
        for m in matrix:
            for h in hdr:
                de_matriks_kolom=h
                inh=getattr(m,h)
                if len(hdr)==kolomteller:
                    kolomteller=0
                kolomteller+=1
                rij+=1
                oorspronkelijkmatriksnummer=decodeer(m.regel,de_matriks_kolom,kolomteller,cellengte=4)       
                create,cre=KluisjesRV.objects.update_or_create(
                    kluisnummer=oorspronkelijkmatriksnummer,
                    kluisje=oorspronkelijkmatriksnummer,
                    topic=m.naam,
                    row=str(rij).zfill(2),
                    col=str(kolomteller).zfill(2),
                )     
                print(m.naam,de_matriks_kolom,inh,h,oorspronkelijkmatriksnummer)
                print('users ===============')
                # voor ieder geregistreerd kluisje een user aanmaken met ww viking123 ==================
        # for k in KluisjesRV.objects.all().exclude(email=None):
        for k in KluisjesRV.objects.all().exclude(email=''):
            print('kluisje-huurder', k.naamvoluit)
            email = k.email
            username = k.naamvoluit #.lower()
            password ='pbkdf2_sha256$390000$YrBnItyjcuUgxrlMGlWFPH$HBlBExsE2C5EcmEmhHvtDTkMl3PH+0E7EQJLrWER4cs=' 
            try:
                user = User.objects.get(email = email)
                k.huurders.add(user)

            except:
                #  als je geen user vindt dan een user aanmaken.
                # user toevoegen als huurder van het kluisje
                if email!='':
                    user = authenticate(request, username=username, password=password)
                    voegtoe,user=User.objects.update_or_create(
                    email = email,
                    is_active=True,
                    last_name=k.naamvoluit,
                    username = username,
                    password=password,
                    )
                    k.huurders.add(voegtoe)
                    k.verhuurd=True
                    k.save()

            try:
                k.huurders.add(voegtoe)
                k.verhuurd=True
                k.save()
            except:
                print(k)
                pass
        print('end users===============')

    print('einde hernummermatriks===============')
    context={}
    return render(request, 'base/home.html', context)

