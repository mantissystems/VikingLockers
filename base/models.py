import datetime
from datetime import datetime   
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# from django.contrib.auth.models import User
KAMER = [
     ('', '--------'),
            ('D', 'D'),
            ('H', 'H'),
]
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    ploeg = models.CharField(max_length=200, null=True)
    locker = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    # bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
SLOT = [
            ('--', '--'),
            ('H', 'hang'),      #gebruiker heeft hangslot
            ('C', 'cijfer'),    #gebruiker heeft cijferslot; code onbekend
            ]
@property
def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
def get_absolute_url(self):
        return reverse("update-user", kwargs={"pk": self.pk})

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Person(models.Model):
    name = models.CharField(max_length=200, null=True)
    onderhuur=models.BooleanField(default=False)
    kamer = models.CharField(max_length=18, choices=KAMER,default='X')  # <===
    wachtlijst=models.BooleanField(default=False)
    hoofdhuurder=models.BooleanField(default=False)
    locker = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    tekst = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

class Ploeg(models.Model):
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(
        User, related_name='teammembers', blank=True)

    def __str__(self):
        return self.name

class Areset(models.Model):
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
    
class Locker(models.Model):
    kluisnummer = models.CharField(max_length=200)
    email = models.CharField(max_length=200,default='--')
    nieuwe_huurder = models.CharField(max_length=200,default='--')
    vorige_huurder = models.CharField(max_length=200,default='--')
    kluisje = models.CharField(max_length=200)
    type = models.CharField(max_length=18, choices=SLOT,default='--')     
    topic = models.CharField(max_length=18,default='----')     
    verhuurd=models.BooleanField(default=False)
    opgezegd=models.BooleanField(default=False)
    obsolete=models.BooleanField(default=False)
    tekst = models.TextField(blank=True)
    sleutels = models.CharField(max_length=18,default='----')     
    code = models.CharField(max_length=18,default='----')     
    created = models.DateTimeField(auto_now_add=True)
    opzegdatum = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['kluisnummer']
    def __str__(self):
        return self.kluisnummer
    
    def get_next(self):
        next = Locker.objects.filter(id__gt=self.id).order_by('id').first()
        if next:
            return next
    # If the current card is the last one, return the first card in the deck
        else:
            return Locker.objects.all().order_by('id').first()     
        
class Facturatielijst(models.Model):
    kluisnummer = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    in_excel = models.CharField(max_length=200,default='----')     
    renum = models.CharField(max_length=200, null=True)
    is_registered = models.CharField(max_length=200,default='----')     
    type = models.CharField(max_length=18, choices=SLOT,default='--')     
    obsolete=models.BooleanField(default=False)
    sleutels = models.CharField(max_length=18,default='----')     
    code = models.CharField(max_length=18,default='----')     
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']

class Excellijst(models.Model):
    kluisnummer = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    excel = models.CharField(max_length=200,default='----')     
    type = models.CharField(max_length=18, choices=SLOT,default='--')     
    sleutels = models.CharField(max_length=18,default='----')     
    code = models.CharField(max_length=18,default='----')     
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['email']

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Bericht(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Helptekst(models.Model):
    title = models.CharField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    seq = models.CharField(max_length=18,default='----')     
    publish=models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)