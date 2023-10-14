from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name="home"),
    path('activity/', views.activityPage, name="activity"),
    path('info/', views.infoPage, name="info"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('update-user/', views.updateUser, name="update-user"),
    path('update-user2/<str:pk>', views.EditUser.as_view(), name="update-user2"),    #<==
    path('delete-user/<str:pk>',views.UserDeleteView.as_view(),name='delete-user'),
    path('update-usermail//<str:kluis>/', views.updateUser_email.as_view(), name="update-usermail"),
    path('update-person/<str:pk>', views.PersonUpdate_id.as_view(), name="update-person"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('profile/', views.myProfile, name="profile"),
    path('topics/', views.topicsPage, name="topics"),
    path('users/', views.MemberListView.as_view(), name="users"),
    path('profiles/',login_required(views.PersonListView.as_view()),name='profiles'),
    path('wacht-lijst/',views.Wachtlijst.as_view(),name='wacht-lijst'),
    path('lockers/', views.lockersPage2, name="lockers"),
    path('onverhuurd/', views.lockersPage3, name="onverhuurd"),
    path('create-person/', views.CreatePerson.as_view(), name="create-person"),          # <=================
    path('create-locker/', views.CreateLocker.as_view(), name="create-locker"),
    path('<str:pk>/update-locker/',views.update_locker, name='update-locker'),  #        #<==================
    path('<str:pk>/update-locker2/',views.LockerUpdate.as_view(), name='update-locker2'),  # <==== tweede stap
    path('delete-person/<str:pk>',views.PersonDeleteView.as_view(),name='delete-person'),
    path('delete-locker/<str:pk>',views.LockerDeleteView.as_view(),name='delete-locker'),
    path('delete-factuur/<str:pk>',views.FactuurDeleteView.as_view(),name='delete-factuur'),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('delete-bericht/<str:pk>/', views.deleteBericht, name="delete-bericht"),
    path('<str:pk>/excel-regel/',views.excel_regelPage, name='excel-regel'),  
    path('helptekst/', views.helpPage, name='helptekst'),
    path('berichten/', views.berichtenPage, name="berichten"),
    path('export_onverhuurd/', views.export_onverhuurd, name="export_onverhuurd"),
    path('export_verhuurd/', views.export_verhuurd, name="export_verhuurd"),
    path('export_emaillijst/', views.export_emaillijst, name="export_emaillijst"),
    path('facturatielijst/', views.FacturatieView.as_view(), name="facturatielijst"),
    path('edit-factuur/<str:pk>', views.EditFactuur.as_view(), name="edit-factuur"),
    path('create-factuur/', views.CreateFactuur.as_view(), name="create-factuur"),
    path('excellijst/', views.ExcelView.as_view(), name="excellijst"),
   path('m2/', views.m2mtotext, name="m2"),  #creates user from locker mail address
   path('m3/', views.m3, name="m3"), #puts usermail in locker
    # path('<str:pk>/locker/',views.lockerPage, name='locker'),  
#    path('m4/', views.m4, name="m4"),
    ]
    # path('wachtlijst/', views.CreatePerson.as_view(), name="wachtlijst"), 
    # path('<str:pk>/update-locker/',views.update_locker, name='update-locker'),  
    #  path('aantalregistraties/', views.tel_aantal_registraties, name='aantalregistraties'),
    #  path('nummering/', views.nummering, name='nummering'),
# https://docs.djangoproject.com/en/3.1/topics/http/urls/