from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import  User
from .models import  Topic
from .models import Note,Vikinglid,Activiteit,KluisjesRV
admin.site.register(Topic)
admin.register(User)
admin.site.register(Activiteit)
@admin.register(KluisjesRV)
class KluisAdmin(admin.ModelAdmin):
    list_filter = ('topic','kluisnummer')
    list_display = ('naamvoluit', 'kluisnummer','kastje','topic','verhuurd')
    search_fields = ('naamvoluit','kluisnummer')

@admin.register(Vikinglid)
class VikinglidAdmin(admin.ModelAdmin):
    list_filter = ('created','updated')
    list_display = ('id','name', 'email')
    search_fields = ('name','email')