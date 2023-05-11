"""CryptoCurrencyTeller URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('hp.urls')),
    path('Bitcoin/',include('hp1.urls')),
    path('Ethereum/',include('hp2.urls')),
    path('Ripple/',include('hp3.urls')),
    path('Avalanche/',include('hp4.urls')),
    path('Dogecoin/',include('hp5.urls')),
    path('pBit/',include('p1.urls')),
    path('pEth/',include('p2.urls')),
    path('pXrp/',include('p3.urls')),
    path('pAave/',include('p4.urls')),
    path('pDoge/',include('p5.urls')),
    
    
]
