from django.urls import path
from . import views


urlpatterns = [
    path('', views.shipping_options, name='shipping_options'),    
]