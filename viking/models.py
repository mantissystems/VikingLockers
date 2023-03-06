from datetime import datetime
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
SOORT = [
            ('--', '--'),
            ('kluis', 'kluis'),
            ('ploeg', 'ploeg'),
]
SLOT = [
            ('--', '--'),
            ('H', 'hang'),      #gebruiker heeft hangslot
            ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
            ('E', 'eigen'),     #gebruiker heeft eigen slot gebruikt
            ('V', 'Viking(hang)'),  #gebruiker heeft hangslot van Viking
            ]

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
    participants = models.ManyToManyField(User, related_name='participant', blank=True)
    updated = models.DateTimeField(auto_now=True) # everytime save (or updated) the field
    created = models.DateTimeField(auto_now_add=True) # first time created the field

    class Meta:
        ordering = ['name', '-created'] # ('-' for reverse the order)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # when room delete, delete all chiled messages
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)     

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=100)
    avatar=models.ImageField(null=True,default="avatar.svg")      # install Pillow is needed
    email = models.CharField(max_length=100,blank=True)
    # is_flex = models.BooleanField(default=True)        #wil ingedeeld worden in flexpoule
    # is_host = models.BooleanField(default=False)        #kan flexhost zijn
    # keuzes = models.IntegerField(default=0) #aantal keren als host gekozen
    # roeileeftijd = models.CharField(max_length=20,blank=True)
    is_lid= models.BooleanField(default=True)           #is roeiend lid;member
    # in_poule = models.BooleanField(default=False)       #wil flexibel roeiern
    # vaart = models.BooleanField(default=False)          #zit in ingedeelde boot op het water
    # coach = models.CharField(max_length=18, choices=SCULL,default='st1')     
    keuzes = models.IntegerField(default=0) #aantal keren als host gekozen
    # lnr = models.IntegerField(default=0) #lotingnummer 

    def __str__(self):
        return self.name


    def __str__(self):
        return "%s" % (self.event_text)          


class Activiteit(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=18, choices=SOORT,default='--')     
    def __str__(self):
        return self.name

    # def __str__(self):
    #     return "%s" % (self.event_text)               
class Vikinglid(models.Model):
    name = models.CharField(max_length=100)
    avatar=models.ImageField(null=True,default="avatar.svg")      # install Pillow is needed
    email = models.CharField(max_length=100,blank=True)
    description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
    is_lid_van = models.ManyToManyField(Activiteit, related_name='lid_van', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name

     
# class Rooster(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
#     datum = models.DateField(auto_now=False)
#     pub_time = models.CharField(max_length=35, default='10:00')
#     lid = models.ManyToManyField(User, related_name='taak', blank=True)
#     created = models.DateTimeField(default=datetime.now, blank=True)
#     lnr = models.IntegerField(default=0) #loting nummer
#     rnr = models.IntegerField(default=0) #rangnummer



#     def __str__(self):
#         return "%s" % (self.name)               


class Kluis(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    body = models.TextField()
    name = models.CharField(max_length=200)
    location = models.TextField(null=True, blank=True)
    # topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    topic = models.CharField(max_length=18, default='XXX')     
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)     
    # owners = models.ManyToManyField(User, related_name='owner', blank=True)
    slot = models.CharField(max_length=18, choices=SLOT,default='H')     
    sleutels = models.IntegerField(default=2)
    code = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body

# python .\manage.py makemigrations
# python .\manage.py migrate
# class Flexrecurrent(models.Model):
#     regels = models.CharField(max_length=18,default='30')

# class Instromer(models.Model):
#     # user = models.OneToOneField(User, on_delete=models.CASCADE)    
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

from django.db import models

# Create your models here.


class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # info = models.CharField(max_length=35, default='===')
    # owner = models.CharField(max_length=35, default='___')


    def __str__(self):
        return self.body[0:50]
