from django.urls import path
from . import views
# from viking.views import( 
# home,
# loginPage, logoutUser,
# registerPage , 
# topicsPage ,  updateUser,  
#  urv_loginPage ,
#  check_matriks,
# createVikinglid,deleteVikinglid, 
# deleteMessage,
# mutatie,export_team_data,Blokken,
# get_kluis,update_kluis,hernummermatriks,kluis,file_load_view,verhuurPage,
# KluisList,
# )

urlpatterns = [
    path('', views.home, name="home"),
    path('activity/', views.activityPage, name="activity"),
    path('room/<str:pk>/', views.room, name="room"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('update-user/', views.updateUser, name="update-user"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('topics/', views.topicsPage, name="topics"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
     path('create-room/', views.createRoom, name="create-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('<str:pk>/kluis/',views.kluis, name='kluis'),  
    path('<str:pk>/update_kluis/<str:kol>/',views.update_kluis, name='update_kluis'),  
    # path('topics/', topicsPage, name="topics"),
    # path('verhuur/', verhuurPage, name="verhuur"),
    # path('', home, name='home'),
    # path('viking', home, name='home'),
    # path('update-user/', updateUser, name="update-user"),
    # path('register/', registerPage, name="register"),    
    # path('profile/<str:pk>/', userProfile, name='user-profile'),
    # path('create-vikinglid/', createVikinglid, name='create-vikinglid'),
    # path('mutatie/', mutatie, name='mutatie'),
    # path('delete-vikinglid/<str:pk>/', deleteVikinglid, name='delete-vikinglid'),
    #  path('blokken/', Blokken.as_view(), name='blokken'),
    #  path('kluislijst/', KluisList.as_view(), name='kluislijst'),
    # path('<str:pk>/update_kluis/<str:kol>/',update_kluis, name='update_kluis'),  
    # path('<str:pk>/kluis/',kluis, name='kluis'),  
    # path('checkmatriks/', check_matriks, name='checkmatriks'),
    # path('hernummermatriks/', hernummermatriks, name='hernummermatriks'),
    # path('export/', file_load_view, name='export'),
    ]
# https://docs.djangoproject.com/en/3.1/topics/http/urls/