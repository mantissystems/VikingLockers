from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    ploeg = models.CharField(max_length=200, null=True)
    locker = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

SLOT = [
            ('--', '--'),
            ('H', 'hang'),      #gebruiker heeft hangslot
            ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
            ]

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Ploeg(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class Matriks(models.Model):    #wrongly spelled on purpose
    naam= models.CharField(max_length=18,default='matriks')     
    ronde = models.CharField(max_length=200)
    kop = models.CharField(max_length=200)
    regel = models.CharField(max_length=200)
    x_as = models.IntegerField(default=2)
    y_as = models.IntegerField(default=2)
    kol1= models.CharField(max_length=18,default='000')     
    kol2= models.CharField(max_length=18,default='000')     
    kol3= models.CharField(max_length=18,default='000')     
    kol4= models.CharField(max_length=18,default='000')     
    kol5= models.CharField(max_length=18,default='000')     
    kol6= models.CharField(max_length=18,default='000')     
    kol7= models.CharField(max_length=18,default='000')     
    kol8= models.CharField(max_length=18,default='000')     
    kol9= models.CharField(max_length=18,default='000')     
    kol10= models.CharField(max_length=18,default='000')     
    kol11= models.CharField(max_length=18,default='000')     
    kol12= models.CharField(max_length=18,default='000')     
    kol13= models.CharField(max_length=18,default='000')     

class Locker(models.Model):
    kluisnummer = models.CharField(max_length=200)
    # host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=200)
    kluisje = models.CharField(max_length=200)
    type = models.CharField(max_length=18, choices=SLOT,default='--')     
    topic = models.CharField(max_length=18,default='----')     
    row = models.CharField(max_length=18,default='----')     
    col = models.CharField(max_length=18,default='----')     
    verhuurd=models.BooleanField(default=False)
    owners = models.ManyToManyField(User, related_name='owners', blank=True)
    sleutels = models.CharField(max_length=18,default='----')     
    code = models.CharField(max_length=18,default='----')     
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['kluisnummer']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
