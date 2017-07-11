from django.conf.urls import url, include
from .views import student_home, student_login, student_signup

urlpatterns = [
	url(r'^home/$', student_home, name='student_home'),
	url(r'^login/$', student_login, name='student_login'),
	url(r'^signup/$', student_signup, name='student_signup'),
]
