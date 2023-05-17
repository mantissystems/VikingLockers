# from datetime import datetime
# from datetime import date
# from django.db import models
# # from django.contrib.auth.models import User
# # from base.models import User
# from django.utils import timezone
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

# class Matriks(models.Model):    #wrongly spelled on purpose
#     naam= models.CharField(max_length=18,default='matriks')     
#     ronde = models.CharField(max_length=200)
#     kop = models.CharField(max_length=200)
#     regel = models.CharField(max_length=200)
#     x_as = models.IntegerField(default=2)
#     y_as = models.IntegerField(default=2)
#     kol1= models.CharField(max_length=18,default='000')     
#     kol2= models.CharField(max_length=18,default='000')     
#     kol3= models.CharField(max_length=18,default='000')     
#     kol4= models.CharField(max_length=18,default='000')     
#     kol5= models.CharField(max_length=18,default='000')     
#     kol6= models.CharField(max_length=18,default='000')     
#     kol7= models.CharField(max_length=18,default='000')     
#     kol8= models.CharField(max_length=18,default='000')     
#     kol9= models.CharField(max_length=18,default='000')     
#     kol10= models.CharField(max_length=18,default='000')     
#     kol11= models.CharField(max_length=18,default='000')     
#     kol12= models.CharField(max_length=18,default='000')     
#     kol13= models.CharField(max_length=18,default='000')     

# # id,name,email,is_flex,keuzes,is_host
# class File(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(unique=True, null=True)
#     bio = models.TextField(null=True)
    
#     def __str__(self):
#         return self.name

# class KluisjesRV(models.Model):
#     kluisnummer = models.CharField(max_length=200)
#     naamvoluit = models.CharField(max_length=200)
#     gender = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     userid = models.CharField(max_length=200)
#     kluisje = models.CharField(max_length=200)
#     kastje = models.CharField(max_length=18,default='kast1')     
#     label = models.CharField(max_length=18,default='label')     
#     # type = models.CharField(max_length=18, choices=SLOT,default='--')     

#     topic = models.CharField(max_length=18,default='----')     
#     row = models.CharField(max_length=18,default='----')     
#     col = models.CharField(max_length=18,default='----')     
#     verhuurd=models.BooleanField(default=False)
#     huurders = models.ManyToManyField(Instromer, related_name='huurders', blank=True)
#     class Meta:
#         ordering = ['kluisnummer']