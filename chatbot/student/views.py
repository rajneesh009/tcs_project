from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from user.forms import AccountForm
from user.models import CustomUser
from student.forms import StudentLoginForm, StudentSignupForm
from student.models import Student
import os, re, datetime, logging
from bs4 import BeautifulSoup


# Create your views here.

@require_POST
def student_login(request):
	f = StudentLoginForm(request.POST)
	if f.is_valid():
		user = f.get_user()
		auth_login(request, user)
		context = {'user' : user }
		return redirect('home')
	else:
		return JsonResponse(status=400, data={'errors': dict(f.errors.items())})

@require_POST
def student_signup(request):
	f = StudentSignupForm(request.POST)
	if f.is_valid():
		user = f.save()
		user = authenticate(username=f.cleaned_data['username'], password=f.cleaned_data['password2'])
#		auth_login(request, user)
		context = {'user': user }
		return render(request, 'user/post_signup.html', context)
	else:
		return JsonResponse(status=400, data={'errors': dict(f.errors.items())})


@login_required
@require_GET
def student_home(request, **kwargs):
##	if request.user.type == 'S':
	context = {}
	user = request.user
	student = request.user.student
	context = {'student' : student }
	return render(request, 'student/home.html', context)
##	else:
##		return handle_user_type(request, redirect_request=True)


