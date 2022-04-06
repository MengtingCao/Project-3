from django.urls import path, include

from django.contrib import admin
from . import views

urlpatterns = [
    
    path('', views.index, name = 'index'),
    path('messages/send/', views.send),
    path('messages/update/', views.update, name= 'update'),
    path('messages/', views.messages, name="messages"),
    path('messages/updateM/', views.updateM, name="updateM"),
    path('messages/updategmID/', views.updategmID, name="updategmID"),
    path('gmlogin/', views.groupMe_login, name='GroupMe_Login'),
    path('groupmeauth/',views.groupMe_auth, name='groupmeauth'),
    path('login', views.login_view,name="login"),
    path('signup', views.signup_view,name="signup"),

]