from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message,KluisjesRV,Matriks,Locker
from base.models import User,AbstractUser
# admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
@admin.register(Matriks)
class matriksAdmin(admin.ModelAdmin):
    list_filter = ('naam','regel')
    list_display = ('naam','regel')
    search_fields = ('naam','regel')
@admin.register(KluisjesRV)
class kluisAdmin(admin.ModelAdmin):
    list_filter = ('topic','kluisnummer')
    list_display = ('topic','kluisnummer')
    search_fields = ('topic','kluisnummer','email')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active','is_staff')
    list_display = ('last_name','email')
    search_fields = ('last_name','email')
@admin.register(Locker)
class kluisAdmin(admin.ModelAdmin):
    list_filter = ('topic','kluisnummer')
    list_display = ('topic','kluisnummer')
    search_fields = ('topic','kluisnummer','email')
