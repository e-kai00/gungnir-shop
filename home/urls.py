from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('announcement/', views.announcement, name='announcement'),
]