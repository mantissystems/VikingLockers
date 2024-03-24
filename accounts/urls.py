from django.urls import path
from accounts import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profile/', views.myProfile, name="profile"),
]