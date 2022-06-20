from django.contrib import admin
from django.urls import path, include
from notesapp import views

urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.ulogin,name="ulogin"),
    path('register',views.register,name="register"),
    path('logout',views.ulogout,name="ulogout"),
    path('addnote',views.addnote,name="addnote"),
    # path('addtag',views.addtag,name="addtag"),
    path('<int:nid>',views.notedisplay,name="notedisplay"),
    path('<int:nid>/editnote',views.editnote,name="editnote"),
]