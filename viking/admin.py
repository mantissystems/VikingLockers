from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import  User
from .models import  Topic
from .models import Room, Message,Note,Vikinglid,Activiteit,Kluis
admin.site.register(Topic)
admin.site.register(Message)
# admin.site.register(Note)
# admin.site.register(Instromer)
admin.register(User)
# admin.register(Person)
admin.site.register(Vikinglid)
admin.site.register(Activiteit)
admin.site.register(Room)
@admin.register(Kluis)
class KluisAdmin(admin.ModelAdmin):
    list_filter = ('slot','location')
    list_display = ('name', 'slot','location','user_id','sleutels')
    search_fields = ('slot','location')

# @admin.register(Note)
# class NoteAdmin(admin.ModelAdmin):
#     list_filter = ('body','id')
#     list_display = ('body', 'id')

# admin.site.register(Kluis)
