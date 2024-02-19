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
    path('delete-user/<str:pk>',views.UserDeleteView.as_view(),name='delete-user'),
    path('update-usermail//<str:kluis>/', views.updateUser_email.as_view(), name="update-usermail"),
    path('update-user/', views.updateUser, name="update-user"),
    path('update-user2/<str:pk>', views.EditUser.as_view(), name="update-user2"),    #<==
    path('update-person/<str:pk>', views.PersonUpdate_id.as_view(), name="update-person"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('profile/', views.myProfile, name="profile"),
    path('topics/', views.topicsPage, name="topics"),
    path('users/', views.MemberListView.as_view(), name="users"),
    path('profiles/',login_required(views.PersonListView.as_view()),name='profiles'),
    path('wacht-lijst/',views.Wachtlijst.as_view(),name='wacht-lijst'),
    path('lockers/', views.lockersPage2, name="lockers"),
    path('lockerview',views.LockerListView.as_view(),name='lockerview'),
    path('requests',views.RequestView.as_view(),name='requests'),
    path('tools/',views.tools, name='tools'),  
    path('onverhuurd/', views.lockersPage3, name="onverhuurd"),
    path('verhuurd/', views.LockerView.as_view(), name="verhuurd"),
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
    path('facturatielijst/', views.FacturatieView.as_view(), name="facturatielijst"),
    path('edit-factuur/<str:pk>', views.EditFactuur.as_view(), name="edit-factuur"),
    path('create-factuur/', views.CreateFactuur.as_view(), name="create-factuur"),
    path('excellijst/', views.ExcelView.as_view(), name="excellijst"),
    path('huuropzeggen/<str:pk>', views.huuropzeggen, name="huuropzeggen"),
    path('t1/', views.createAreset, name="t1"),  #werkzaamheden
    path('t2/<str:pk>/', views.areset, name="t2"),
    path('t3/',views.TimesheetView.as_view(),name='t3'), #timesheet list
    path('delete-t2/<str:pk>/', views.deleteaReset, name="delete-t2"),
    path('t4/<str:pk>', views.room_start, name="t4"),
    path('vervolg/', views.vervolg, name="vervolg"),
    path('update-vervolg/<str:pk>/', views.update_vervolg, name="update-vervolg"),
    path('stop/', views.stop, name="stop"),
    path('end/', views.end, name="end"),
    path('room-clear/<str:pk>', views.clear_tijdregels, name="room-clear"),

   path('m2/', views.m2mtotext, name="m2"),  #creates user from locker mail address if no user exists
   path('m3/', views.m3, name="m3"), #puts usermail in get locker by email
   path('m5/', views.m5, name="m5"), #check facturatielijst in get locker by email
   path('m6/<str:pk>', views.m6, name="m6"), #check facturatielijst in get locker by email
    path('all_lockers/',views.all_entrantsPage, name='all_lockers'),  
    ]
    # path('export_emaillijst/', views.export_emaillijst, name="export_emaillijst"),
    # path('export_wachtlijst/', views.export_wachtlijst, name="export_wachtlijst"),
    # path('polls_results/<int:question_id>/', views.polls_results, name='polls_results'),
#    path('m4/', views.m4, name="m4"), #puts usermail in get locker by email
    # path('export_verhuurd/', views.export_verhuurd, name="export_verhuurd"),
    # path('export_onverhuurd/', views.export_onverhuurd, name="export_onverhuurd"),
    #  path('aantalregistraties/', views.tel_aantal_registraties, name='aantalregistraties'),
    #  path('nummering/', views.nummering, name='nummering'),
# https://docs.djangoproject.com/en/3.1/topics/http/urls/