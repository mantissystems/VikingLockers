from django.urls import path
from . import views
from viking.views import( 
home,
loginPage, logoutUser,
registerPage , 
topicsPage ,  updateUser, userProfile,
 urv_loginPage ,
 check_matriks,
createVikinglid,deleteVikinglid, 
aanvrage,export_team_data,Blokken,get_matrix,get_kluis,update_kluis,hernummermatriks,kluis,file_load_view,some_view,verhuurPage, 
)
urlpatterns = [
    path('', home, name='home'),
    path('viking', home, name='home'),
    path('login/', urv_loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('topics/', topicsPage, name="topics"),
    path('verhuur/', verhuurPage, name="verhuur"),
    path('update-user/', updateUser, name="update-user"),
    path('register/', registerPage, name="register"),    
    path('profile/<str:pk>/', userProfile, name='user-profile'),
    path('create-vikinglid/', createVikinglid, name='create-vikinglid'),
    path('create-aanvrage/', aanvrage, name='create-aanvrage'),
    path('delete-vikinglid/<str:pk>/', deleteVikinglid, name='delete-vikinglid'),
    path('notes/', views.getNotes, name="notes"),
    path('api/topics/', views.getTopics, name="topicsapi"),
    path('notes/<str:pk>/', views.getNote, name="note"),
     path('blokken/', Blokken.as_view(), name='blokken'),
    path('get_matrix/',get_matrix, name='get_matrix'),  
    # path('<str:pk>/set_kluis/<str:kol>',set_kluis, name='set_kluis'),  
    path('<str:pk>/update_kluis/<str:kol>/',update_kluis, name='update_kluis'),  
    path('<str:pk>/kluis/',kluis, name='kluis'),  
    path('checkmatriks/', check_matriks, name='checkmatriks'),
    path('hernummermatriks/', hernummermatriks, name='hernummermatriks'),
    path('export/', file_load_view, name='export'),
    path('eksporteer/', some_view, name='eksporteer'),
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/