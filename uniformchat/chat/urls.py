from django.urls import path, include

from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('tutorials/', views.tutorials,name="tutorials"),
    path('messages/send/', views.send),
    path('messages/sendslack/', views.sendslack),
    path('messages/adddiscchat/discadd/', views.disc_add),
    path('messages/adddiscchat/discdelete/', views.deletedchann),
    path('messages/addslackchat/slackadd/', views.slack_add),
    path('messages/addslackchat/slackdelete/', views.deleteschann),
    path('messages/update/', views.update, name= 'update'),
    path('messages/', views.messages, name="messages"),
    path('messages/updateM/', views.updateM, name="updateM"),
    path('messages/updateMload/', views.updateMload, name="updateMload"),
    path('messages/updategmID/', views.updategmID, name="updategmID"),
    path('messages/updatediscID/', views.updatediscID, name="updatediscID"),
    path('messages/updateslackID/', views.updateslackID, name="updateslackID"),
    path('gmlogin/', views.groupMe_login, name='GroupMe_Login'),
    path('groupmeauth/',views.groupMe_auth, name='groupmeauth'),
    path('messages/readall/',views.read_all, name='readall'),
    path('disclogin/', views.discord_login, name='discord_Login'),
    path('discordauth/',views.discord_auth, name='discordauth'),
    path('slacklogin/', views.slack_login, name='slack_Login'),
    path('slackauth/', views.slack_auth, name= "slackauth"),
    path('login/', views.login_view,name="login"),
    path('logout/', views.logout_view,name="logout"),
    path('messages/logout/', views.logout_view,name="logout"),
    path('messages/auth/', views.authhub,name="authhub"),
    path('messages/adddiscchat/', views.adddiscchat,name="adddiscchat"),
    path('messages/addslackchat/', views.addslackchat,name="addslackchat"),
    path('signup/', views.signup_view,name="signup"),

]
