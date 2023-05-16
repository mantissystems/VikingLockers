from datetime import datetime
from datetime import date
from django.db import models
# from django.contrib.auth.models import User
# from base.models import User
from django.utils import timezone
# SOORT = [
#             ('--', '--'),
#             ('kluis', 'kluis'),
#             ('ploeg', 'ploeg'),
# ]
# SLOT = [
#             ('--', '--'),
#             ('H', 'hang'),      #gebruiker heeft hangslot
#             ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
#             ]

# class Topic(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name


# class Instromer(models.Model):
#     name= models.CharField(max_length=222,default='---')     
#     # updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['name', ]
#     def __str__(self):
#         return self.name
    
# class Vikinglid(models.Model):
#     name = models.CharField(max_length=100)
#     avatar=models.ImageField(null=True,default="avatar.svg")      # install Pillow is needed
#     email = models.CharField(max_length=100,blank=True)
#     description = models.TextField(null=True, blank=True) # database field (can Empty), form field (can Empty)
#     # is_lid_van = models.ManyToManyField(Activiteit, related_name='lid_van', blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         ordering = ['name', '-updated']
#     def __str__(self):
#         return self.name
    
# from django.db import models

# class Note(models.Model):
#     body = models.TextField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body[0:50]
    

# class Kluislabel(models.Model):
#     name = models.TextField(null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
