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

class Activiteit(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=18, choices=SOORT,default='--')     
    def __str__(self):
        return self.name

class Vikinglid(models.Model):
    name = models.CharField(max_length=100)
    avatar=models.ImageField(null=True,default="avatar.svg")      # install Pillow is needed
    email = models.CharField(max_length=100,blank=True)
    description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
    is_lid_van = models.ManyToManyField(Activiteit, related_name='lid_van', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name', '-updated']
    def __str__(self):
        return self.name

class Kluis(models.Model):
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)     
    user_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    location = models.TextField(null=True, blank=True)
    slot = models.CharField(max_length=18,default='H')     
    sleutels = models.IntegerField(default=2)
    code = models.TextField(null=True, blank=True)
    topic_id = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body

from django.db import models

class Note(models.Model):
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
