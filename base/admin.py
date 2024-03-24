from django.contrib import admin
# Register your models here.
from .models import  Topic, Message,Locker,Ploeg,Helptekst,Bericht,Person,Facturatielijst,Areset,Tijdregel
# from base.models import User,AbstractUser
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

class PersonadminResource(resources.ModelResource):
    updated=Field()
    verhuurd=Field()
    class Meta:
        model=Person
        fields=['id','name','email','onderhuur','wachtlijst','hoofdhuurder','onderhuur','locker','tekst']
        export_order=['id','name','email','onderhuur','wachtlijst','hoofdhuurder','onderhuur','locker','tekst']
    # def dehydrate_verhuurd(self,obj):
    #     if obj.verhuurd:
    #         return "ja"
    #     return "nee"
    # def dehydrate_updated(self,obj):
    #     return obj.updated.strftime("%d-%m-%Y %H:%M:%S")

admin.site.register(Ploeg)
admin.site.register(Topic)
admin.site.register(Message)
@admin.register(Helptekst)
class helpAdmin(admin.ModelAdmin):
    list_filter = ('title','content')
    list_display = ('title','content','seq','publish')
    search_fields = ('title','content')
@admin.register(Bericht)

@admin.register(Tijdregel)
class TijdregelAdmin(ImportExportModelAdmin):
    pass

# @admin.register(User)
# class UserAdmin(ImportExportModelAdmin):
#     pass
@admin.register(Facturatielijst)
class UserAdmin(ImportExportModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(Areset)
class AresetAdmin(ImportExportModelAdmin):
    pass

    @admin.register(Locker)
    class LockerAdmin(ImportExportModelAdmin):
        pass    