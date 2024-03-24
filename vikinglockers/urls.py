from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve 
urlpatterns = [
    # path('__debug__/', include('debug_toolbar.urls')),        
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path("accounts/", include("accounts.urls")),  # signup page loads first
    path('api/', include('api.urls')),
 ] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # path("accounts/", include("django.contrib.auth.urls")),  # authentication still active
    # path("base/", include("django.contrib.auth.urls")),  # authentication still active
    # path('home/', TemplateView.as_view(template_name='base/home')),

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
