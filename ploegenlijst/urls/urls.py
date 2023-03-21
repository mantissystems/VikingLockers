from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html')),
    path('admin/', admin.site.urls),
    path('', include('viking.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),    
]
# urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#  from proshop_django_master/backend
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', TemplateView.as_view(template_name='index.html')), #from vue after npm run build
#     path('api/products/', include('base.urls.product_urls')),
#     path('api/users/', include('base.urls.user_urls')),
#     path('api/orders/', include('base.urls.order_urls')),
# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)