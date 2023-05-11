from django.urls import path
from . import views


urlpatterns=[
    path('',views.pBit,name='pBit')
]