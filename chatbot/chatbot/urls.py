"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include, static
from django.contrib import admin
from user.views import auth, landing, login, logout, team, scrapingcricket, scrapingfootball, scrapingweather, scrapingstock, scrapingpetrol 
from student.views import student_home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', landing, name='landing'),
    url(r'^auth/$', auth, name='auth'),
    url(r'^home/$', student_home, name='student_home'),
    url(r'^team/$', team, name='team'),
    url(r'^scrapingcricket/', scrapingcricket, name='scrapingcricket'),
    url(r'^scrapingfootball/', scrapingfootball , name='scrapingfootball'),
    url(r'^scrapingweather/', scrapingweather , name='scrapingweather'),
    url(r'^scrapingstock/', scrapingstock , name='scrapingstock'),
    url(r'^scrapingpetrol/', scrapingpetrol , name='scrapingpetrol'),
    url(r'^user/', include('user.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

