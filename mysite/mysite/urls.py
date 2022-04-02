from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]