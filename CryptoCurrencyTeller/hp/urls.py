from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('/',views.signin_evaluate,name='signin_evaluate')
]