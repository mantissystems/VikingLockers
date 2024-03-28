from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from base.models import Bericht
# Create your views here.
def myProfile(request):
    user = request.user
    form = UserCreationForm(instance=user)
    berichten=Bericht.objects.all() # .filter(user=request.user.id)
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
            inspectie=request.POST.get('locker'),
            email=request.POST.get('locker'),
            verhuurd=False,
            kluisje=request.POST.get('locker'))
        if not form.is_valid():
            print('invalid')
        if form.is_valid():
            locker, created = Locker.objects.update_or_create(
            inspectie=request.POST.get('locker'),
            email=user.email,
            verhuurd=False,
            kluisje=request.POST.get('locker'))
            form.save()
            return redirect('update-profile', pk=user.id)
    return render(request, 'base/update-profile.html', context)
