from django.urls import path
from . import views


urlpatterns=[
    path('',views.pEth,name='pEth')
]