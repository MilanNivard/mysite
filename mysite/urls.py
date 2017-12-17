"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('eartraining.urls')),
    url(r'^pitch/', include('pitch.urls')),
    url(r'^intervals/', include('intervals.urls')),
    url(r'^melodic_dictation/', include('melodic_dictation.urls')),
    url(r'^triads/', include('triads.urls')),
    url(r'^seventh_chords/', include('seventh_chords.urls')),
    url(r'^extended_chords/', include('extended_chords.urls')),
    url(r'^progressions/', include('progressions.urls')),
]
