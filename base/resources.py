from import_export import resources
from .models import Locker

class LockerResource(resources.ModelResource):
    class Meta:
        model = Locker