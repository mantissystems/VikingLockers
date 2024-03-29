from django.urls import path
from . import views
app_name = 'api'
urlpatterns = [
    path('routes', views.getRoutes, name="routes"),
    path('notes/', views.getNotes, name="notes"),
    path('inspecties/', views.getInspecties, name="inspecties"),
    path('notes/create/', views.createNote, name="create-note"),
    path('notes/<str:pk>/update/', views.updateNote, name="update-note"),
    path('notes/<str:pk>/delete/', views.deleteNote, name="delete-note"),
    path('notes/<str:pk>/', views.getNote, name="note"),

]
