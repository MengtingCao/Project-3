from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name = 'index'),
    path('send/', views.send),
    path('update/', views.update, name= 'update'),
]