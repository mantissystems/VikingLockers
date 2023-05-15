from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message,KluisjesRV
from base.models import User,AbstractUser
admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(KluisjesRV)