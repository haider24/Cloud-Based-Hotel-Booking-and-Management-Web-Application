"""djangotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from django.conf.urls import  url

from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.test, name='index'),
    url(r'^login/',views.signin,name='login'),
    url(r'^logout/',views.signout,name='logout'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^feedback/',views.feedback,name='feedback'),
    url(r'^rating/',views.rating,name='rating'),
    url(r'^changepassword/',views.changePassword,name='changePassword'),
    url(r'^rooms/',views.rooms,name='rooms'),

]