from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve 
urlpatterns = [
    # path('', TemplateView.as_view(template_name='main.html')),
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),    
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
