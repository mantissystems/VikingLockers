from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import  User
from .models import  Topic
from .models import Note,Vikinglid,Activiteit,Kluis
admin.site.register(Topic)
admin.register(User)
admin.site.register(Activiteit)
@admin.register(Kluis)
class KluisAdmin(admin.ModelAdmin):
    list_filter = ('slot','location')
    list_display = ('name', 'slot','location','user_id','sleutels')
    search_fields = ('slot','location')

@admin.register(Vikinglid)
class VikinglidAdmin(admin.ModelAdmin):
    list_filter = ('created','updated')
    list_display = ('id','name', 'email')
    search_fields = ('name','email')