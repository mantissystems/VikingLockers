from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message,Locker,Ploeg,Helptekst,Bericht
from base.models import User,AbstractUser
admin.site.register(Ploeg)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
@admin.register(Helptekst)
class helpAdmin(admin.ModelAdmin):
    list_filter = ('title','content')
    list_display = ('title','content','seq','publish')
    search_fields = ('title','content')
@admin.register(Bericht)
class kluisAdmin(admin.ModelAdmin):
    list_filter = ('locker','user')
    list_display = ('locker','body')
    search_fields = ('locker','body')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active','is_staff')
    list_display = ('last_name','email')
    search_fields = ('last_name','email')
@admin.register(Locker)
class kluisAdmin(admin.ModelAdmin):
    list_filter = ('topic','kluisnummer')
    list_display = ('topic','kluisnummer','email')
    search_fields = ('topic','kluisnummer','email')
