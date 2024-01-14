from import_export import resources
from .models import Locker,Person

class LockerResource(resources.ModelResource):
    class Meta:
        model = Locker
        
class PersonResource(resources.ModelResource):
    class Meta:
        model = Person        