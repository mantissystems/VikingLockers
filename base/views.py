from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# from viking.models import  Matriks,KluisjesRV
from base.models import Room,Message,User,Topic,Matriks,Locker
from django.db.models import Q
from base.forms import RoomForm, UserForm,  MyUserCreationForm
from django.views.generic import(TemplateView)
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
        # messages.error(request, 'User email already in use.')
        # return render_to_response('template_name', message='Save complete')
        # return HttpResponse('email used')
        info='email already in use'
        return HttpResponseRedirect('/info/',{'info':info,})


    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.last_name = user.username.lower()
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
    from django.contrib import messages
    # messages.add_message(request, messages.INFO, "Hello world.")    
    # messages.add_message(request, messages.INFO, "Over 9000!", extra_tags="dragonball")
    # messages.error(request, "Email box full", extra_tags="email")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    lockers=Matriks.objects.all()     
    from django.db.models import Count
    results = (Locker.objects
    .values('topic')
    .annotate(dcount=Count('topic'))
    .order_by()
    )   
    cabinetsused = (Matriks.objects
    .values('naam')
    .annotate(dcount=Count('regel'))
    .order_by()
    )   
    yourlocker=Locker.objects.none
    joiner=Locker.objects.none
    cnt=0
    joincnt=0
    # print('yourlocker',cabinetsused)
    if request.user != AnonymousUser:
        try:
            user=User.objects.get(id=request.user.id)
            joiner=Locker.objects.filter(owners__email__icontains=user.email)
            yourlocker=Locker.objects.filter(email__icontains=user.email)
            cnt=yourlocker.count()
            joincnt=joiner.count()
            # print('yourlocker',yourlocker,user,cnt,joincnt,cabinetsused[0].dcount)
            # messages.info(request, f'Aantal Cabinetten {cabinetsused} ')
            messages.info(request, f'Huurder van {cnt} lockers')
            if joincnt>0:messages.info(request, f'Onderhuurder van {joincnt} lockers')
        except:
            user=AnonymousUser
            messages.info(request, f'Ubent niet ingelogd. Svp Inloggen / Registreren')
    if q!='' or q !=None:
        rooms_found = Matriks.objects.filter(regel__icontains=q).values_list('naam',flat=True)
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)|
        Q(name__in=rooms_found) 
    ).order_by('name').exclude(name='Wachtlijst')
    if rooms.count() == 1: 
        messages.success(request, f'Searched for locker: {q}')
        print('room id',rooms[0].id)
        url = reverse('room', kwargs={"pk":rooms[0].id})
        #  return reverse('my_named_url', kwargs={ "pk": self.pk }) <---voorbeeld
        return HttpResponseRedirect(url)
    # if rooms.count() >= 1:
        # print('room id',rooms[0].id)
        # url = reverse('home')
        #  return reverse('my_named_url', kwargs={ "pk": self.pk }) <---voorbeeld
        # return HttpResponseRedirect(url)
 
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    for i in range (0,13):
        kopmtrx.append(hdr[i])
    topics = Topic.objects.all()[0:5]
    # room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]   

    context = {'rooms': rooms, 
               'topics': topics,
               'results': results,
                'lockers': lockers,
                'kopmtrx': kopmtrx,
               'cabinetsused': cabinetsused, 
               'yourlocker': yourlocker, 
               'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})

def helpPage(request):
    
    room_messages = Message.objects.all()
    fverhuurd=Q(verhuurd=True)

    verhuurd=Locker.objects.all().filter(fverhuurd)  #verzamel verhuurde kluisjes voor de room 
    used=verhuurd.count()
    context={'room_messages': room_messages,
             'used':used,
             }
    return render(request, 'base/help.html', context)

def infoPage(request):
    
    room_messages = Message.objects.all()
    fverhuurd=Q(verhuurd=True)

    # verhuurd=Locker.objects.all().filter(fverhuurd)  #verzamel verhuurde kluisjes voor de room 
    # used=verhuurd.count()
    context={'room_messages': room_messages,
            #  'used':used,
             }
    return render(request, 'base/info.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    vikingers=User.objects.all().order_by('email')
    topic=room.name

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
    heren=Matriks.objects.filter(naam__icontains=topic).exclude(y_as__in=(7,8,9)).order_by('y_as')
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    kopmtrx=[]
    for i in range (0,9):
        kopmtrx.append(hdr[i])
    if topic=='Wachtlijst':
        hdr=['wachtlijst']
        kopmtrx=hdr
    topics = Topic.objects.all()[0:5]
    q='H35'  #temporary value to test 'highlight' templatetag
    q=' '
    context = {
        'room': room,
               'topics': topics,
                'heren': heren,
                'verhuurd': verhuurd,
                'kopmtrx': kopmtrx,
               'participants': participants,
               'q':q,
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
    rms = Locker.objects.all().filter(verhuurd=True)
    owner_count=0
    rgl=matrix.y_as
    # owners=[]    
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    dematrikskolom=hdr[column];print(dematrikskolom)
    kluisje=getattr(matrix,dematrikskolom)
    matriksnaam=getattr(matrix,'naam')
    opheffen= request.POST.get('opheffen')
    column=int(kol)
    regel=matrix.regel
    oorspronkelijkmatriksnummer=decodeer(regel,dematrikskolom,column,cellengte=3)
    print('oorspronkelijkmatriksnummer',oorspronkelijkmatriksnummer)
    try:
        kls=Locker.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
        # try:
        #     huurders=kls.owners.all()
        #     print(kls,huurders)
        #     if huurders.count()==0: 
        #         messages.error(request, f'{matriksnaam}: Geen huurders verder.')
        #         return redirect('home')
        # except:
        #     pass
    except: 
        Locker.DoesNotExist
        messages.error(request, f'{pk} {kol}: Niet gevonden')
        url = reverse('create_locker', kwargs={'row': pk,'kol': kol})
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        huurder= request.POST.get('heeftkluis')
        label= request.POST.get('kluislabel')
        slot= request.POST.get('slot')
        sleutels= request.POST.get('sleutels')
        code= request.POST.get('code')
        print(sleutels,code)
        your_name= request.POST.get('your_name')
        huuropheffen= request.POST.get('huuropheffen')
        kls.userid=huurder
        kls.verhuurd=True
        # return HttpResponseRedirect('/')
        if slot:
            kls.type=slot
            kls.save()
        if huurder or your_name:
            h=User.objects.get(id=huurder)
            kls.owners.add(h)
            setattr(kls, 'verhuurd',True)
            kls.save()
        if huuropheffen:
            h=User.objects.get(id=huuropheffen)
            print('opheffen',h)
            kls.owners.remove(h)
            setattr(kls, 'verhuurd',False)
            kls.save()
        if sleutels:
            kls.sleutels=sleutels
            kls.save()
        if code:
            kls.code=code
            kls.save()

        return redirect('home')

    vikingers=User.objects.all().order_by('username')
    context = {
                'vikingers':vikingers,
                'kluis': kls,
                'verhuurd': rms,
                # 'huurders': huurders,
                'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer,
            }
    return render(request, 'base/update_kluis_form.html', context)

def kluis(request, pk):
    rms = Locker.objects.all()
    owner_count=0
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    huurders=[]
    opheffen= request.POST.get('opheffen')
    if pk.isnumeric() :
        kls=Locker.objects.get(id=pk)
        huurders=kls.owners
    else:
        kls=Locker.objects.get(kluisnummer=pk)        
        huurders=kls.owners
        if huurders.count()==0: 
            messages.error(request, f'{kls.kluisnummer}: Geen huurders verder.')
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
            kls.owners.add(h)
            setattr(kls, 'verhuurd',True)
            kls.save()
        if huuropheffen:
            h=User.objects.get(id=huuropheffen)
            print('opheffen',h)
            kls.owners.remove(h)
            setattr(kls, 'verhuurd',False)
            kls.save()

        # return redirect('home')

    vikingers=User.objects.all().order_by('username')
    context = {
                'vikingers':vikingers,
                'kluis': kls,
                'huurders': huurders,
            }
    return render(request, 'base/update_kluis_form.html', context)

def decodeer(regel,de_matriks_kolom,column,cellengte):
    begincell=(0+column)*column*cellengte
    eindcell=0+cellengte
    b=0+((column-1)*cellengte)
    e=b+cellengte
    c=regel[b:e] 
    oorspronkelijkmatriksnummer=c

    return oorspronkelijkmatriksnummer

def hernummermatriks_old(request):
    print('in hernummermatriks===============')
    # voor iedere cel in de Matriks per Room een kluisjesRV aanmaken ==================
    hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12',]#'kol13',] #'kol14']
    begincell=0;cellengte=0;eindcell=0;kolomteller=0
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

class Blokken(TemplateView):
    template_name = 'base/home.html'
    def get_context_data(self, **kwargs):
        hdr=['kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12',]#'kol13',] #'kol14']
        # begincell=0;cellengte=0;eindcell=0
        begincell=0;cellengte=0;eindcell=0;kolomteller=0;rij=0
        topics=Room.objects.all().exclude(name='Wachtlijst')
        kasten= topics #['Heren','Adames','Bdames','Cdames','Ddames']
        Matriks.objects.all().delete()
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
                Matriks.objects.update_or_create( 
                        kop=s,
                        regel=s,
                        # ronde=r,
                        # x_as=r,
                        y_as=regelteller,
                        naam=matrixnaam,
                        )    
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
    for r in matrixen:
        print(r)
        matrix=Matriks.objects.filter(naam=r) #.first()
        for m in matrix:
        # m=matrix
            print(m)
            rij=str(m.y_as)
            cellengte=3
            regel=m.regel
            for kol in range(0,len(hdr)):
                de_matriks_kolom=hdr[kol]
                oorspronkelijkmatriksnummer=decodeer(regel,de_matriks_kolom,kol,cellengte)
                print(m.naam,de_matriks_kolom,begincell,oorspronkelijkmatriksnummer)
                setattr(m, de_matriks_kolom, oorspronkelijkmatriksnummer)
                m.save()
        context={}
    return render(request, 'base/home.html', context)

def create_locker(request,row,kol):
    hdr=['', 'kol1','kol2','kol3','kol4','kol5','kol6','kol7','kol8','kol9','kol10','kol11','kol12','kol13']  #LET OP: KOLOM NUL NIET VERGETEN
    column=int(kol)
    print('params',row,kol)
    matrix=Matriks.objects.get(id=row)
    rms = Locker.objects.all()
    rgl=matrix.y_as
    dematrikskolom=hdr[column];print(dematrikskolom)
    kluisje=getattr(matrix,dematrikskolom)
    matriksnaam=getattr(matrix,'naam')
    column=int(kol)
    regel=matrix.regel
    oorspronkelijkmatriksnummer=decodeer(regel,dematrikskolom,column,cellengte=3)
    print('locker:',oorspronkelijkmatriksnummer)
    try:
        l=Locker.objects.get(kluisnummer=oorspronkelijkmatriksnummer)
        regel=l.regel
    except:
        print('except..not found..',regel,dematrikskolom,column,oorspronkelijkmatriksnummer)
        email=request.user.email
        print(row,kol,'create-locker?',email)

        if request.method == 'POST':
            create,cre=Locker.objects.update_or_create(
                            kluisnummer=oorspronkelijkmatriksnummer,
                            kluisje=oorspronkelijkmatriksnummer,
                            topic=matriksnaam,
                            email=email,
                            row=row.zfill(2),
                            col=kol.zfill(2),
                            verhuurd=True
                            )
            create.owners.add(request.user)
            return render(request, 'base/locker-add.html', {'column': kol,'row':row,'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer })
            # return redirect('home')
    return render(request, 'base/locker-add.html', {'column': kol,'row':row,'oorspronkelijkmatriksnummer':oorspronkelijkmatriksnummer })
