from django.urls import path
from . import views

urlpatterns=[
    path('',views.Avalanche,name='Avalanche')
]