from django.conf.urls import url, include
from .views import home, logout, reset_password, forgot_password

urlpatterns = [
		url(r'^home/$', home, name='home'),
		url(r'^logout/$', logout, name='logout'),
		url(r'^forgot_password/$', forgot_password, name='forgot_password'),
]