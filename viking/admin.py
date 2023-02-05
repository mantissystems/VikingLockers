from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import  User
from .models import  Person, Topic
from .models import Room, Message,Person,Instromer,Note,Vikinglid,Activiteit
admin.site.register(Topic)
admin.site.register(Message)
# admin.site.register(Note)
admin.site.register(Instromer)
admin.register(User)
admin.register(Person)
admin.register(Vikinglid)
admin.register(Activiteit)
admin.register(Room)
# @admin.register(Person)
# class PersonAdmin(admin.ModelAdmin):
#     list_filter = ('is_host','name')
#     list_display = ('name', 'email','is_host')
#     search_fields = ('name','is_host')
# @admin.register(Room)
# class PloegAdmin(admin.ModelAdmin):
#     list_filter = ('topic','host')
#     list_display = ('name', 'topic','host')
#     search_fields = ('name','topic')

# @admin.register(Kluis)
# class KluisAdmin(admin.ModelAdmin):
    # list_filter = ('slot','location')
    # list_display = ('name', 'slot','location','user','sleutels')
    # search_fields = ('slot','location')

# @admin.register(Note)
# class NoteAdmin(admin.ModelAdmin):
#     list_filter = ('body','id')
#     list_display = ('body', 'id')

# admin.site.register(Kluis)
