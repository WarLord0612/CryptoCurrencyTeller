from django.urls import path
from . import views

urlpatterns=[
    path('',views.Ripple,name='Ripple')
]