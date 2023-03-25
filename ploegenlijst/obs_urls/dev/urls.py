from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    # path('', TemplateView.as_view(template_name='main.html')),
    path('admin/', admin.site.urls),
    path('', include('viking.urls')),
    path('__debug__/', include('debug_toolbar.urls')),    
]