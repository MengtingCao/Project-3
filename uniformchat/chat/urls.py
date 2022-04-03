from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('send/', views.send),
    path('update/', views.update, name= 'update'),
    path('messages/', views.messages, name="messages"),
    path('messages/updateM/', views.updateM, name="updateM"),
    path('gmlogin/', views.groupMe_login, name='GroupMe_Login'),

]