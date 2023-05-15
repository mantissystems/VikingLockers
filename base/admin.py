from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from .models import Room, Topic, Message,File,KluisjesRV
@admin.register(KluisjesRV)
class FileAdmin(ImportExportModelAdmin):
    pass
