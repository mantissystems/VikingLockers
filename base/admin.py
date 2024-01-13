from django.contrib import admin
# Register your models here.
from .models import Room, Topic, Message,Locker,Ploeg,Helptekst,Bericht,Excellijst,Person,Facturatielijst
from base.models import User,AbstractUser
from import_export import resources
from import_export.fields import Field 
from import_export.admin import ImportExportModelAdmin


class LockeradminResource(resources.ModelResource):
    updated=Field()
    verhuurd=Field()
    class Meta:
        model=Locker
        fields=('id','kluisnummer','email','tekst','verhuurd','updated')
        export_order=('id','kluisnummer','email','tekst','verhuurd','updated')
    def dehydrate_verhuurd(self,obj):
        if obj.verhuurd:
            return "ja"
        return "nee"
    def dehydrate_updated(self,obj):
        return obj.updated.strftime("%d-%m-%Y %H:%M:%S")

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
    list_filter = ('user','user')
    list_display = ('user','body')
    search_fields = ('user','body')
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_active','is_staff')
    list_display = ('username','last_name','email','locker')
    search_fields = ('last_name','email','locker')
@admin.register(Person)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('onderhuur','hoofdhuurder','wachtlijst')
    list_display = ('name','email','created')
    search_fields = ('name','email')
    @admin.register(Locker)
    class LockerAdmin(ImportExportModelAdmin):
        pass    
# @admin.register(Locker)
# class kluisAdmin(admin.ModelAdmin):
#     list_filter = ('verhuurd','kluisnummer','obsolete')
#     list_display = ('topic','kluisnummer','email','verhuurd','obsolete','sleutels')
#     search_fields = ('topic','kluisnummer','email')
@admin.register(Excellijst)
class kluisAdmin(admin.ModelAdmin):
    list_filter = ('email','kluisnummer','excel')
    list_display = ('kluisnummer','excel','email')
    search_fields = ('kluisnummer','email','excel')
@admin.register(Facturatielijst)
class factuurAdmin(admin.ModelAdmin):
    list_filter = ('email','in_excel','is_registered')
    list_display = ('email','kluisnummer','in_excel','type')
    search_fields = ('email','type')
