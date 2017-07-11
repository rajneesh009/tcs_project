from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from user.forms import AccountForm, LoginForm, SignupForm
from user.models import CustomUser


# Create your views here
@require_GET
def landing(request):
	context = {'login_form': LoginForm()}	
	return render(request, 'user/landing.html', context)

@require_GET
def auth(request):
	context = {'signup_form': SignupForm()}
	return render(request, 'user/signup.html', context)

@require_GET
def team(request):
	return render(request, 'user/team.html', {})
		

@require_POST
def login(request):
	f = LoginForm(request.POST)
	if f.is_valid():
		user = f.get_user()
		if not user.is_active:
			return JsonResponse(data={'success': True, 'render': loader.render_to_string('account/inactive.html', {'user': user})})
		auth_login(request, user)
		return JsonResponse(data = {'success': True, 'location': get_relevant_reversed_url(request)})
	else:
		return JsonResponse(status=400, data={'errors': dict(f.errors.items())})


@require_http_methods(['GET', 'POST'])
def forgot_password(request):
	if request.user.is_authenticated():
		return redirect(settings.HOME_URL[request.user.type])
	if request.method == 'GET':
		f = ForgotPasswordForm()
	if request.method == 'POST':
		f = ForgotPasswordForm(request.POST)
		if f.is_valid():
			email = f.cleaned_data['email']
			user = CustomUser.objects.filter(email=email).values('pk')
			if user.exists():
				send_forgot_password_email_task.delay(user[0]['pk'], get_current_site(request).domain)
			context = { 'email' : email }
			return render(request, 'account/forgot_password_email_sent.html',context)
	context = {'forgot_password_form' : f}
	return render(request, 'account/forgot_password.html', context)

@require_http_methods(['GET', 'POST'])
def reset_password(request, user_hashid='', token=''):
	if request.user.is_authenticated():
		return redirect(settings.HOME_URL[request.user.type])
	try:
		uid = settings.HASHID_CUSTOM_USER.decode(user_hashid)[0]
	except IndexError:
		return render(request, '404.html')
	try:
		user = CustomUser.objects.get(pk=uid)
	except CustomUser.DoesNotExist:
		return render(request, '404.html')
	if not default_token_generator.check_token(user, token):
		context = {'validlink': False}
		return render(request, 'account/set_password.html', context)
	if request.method == 'GET':
		f = SetPasswordForm()
	else:
		f = SetPasswordForm(request.POST)
		if f.is_valid():
			user.set_password(f.cleaned_data['password1'])
			user.save()
			accountLogger.info('Password has been reset for user %s' % user.username)
#			return redirect('login')
			return render(request, 'account/set_password.html', {'successful': True})
	context = { 'validlink': True, 'password_reset_form': f, 'user_hashid': user_hashid, 'token': token}
	return render(request, 'account/set_password.html', context)


@login_required
@require_GET
def home(request):
	return handle_user_type(request, redirect_request=True)

@login_required
@require_GET
def logout(request):
	auth_logout(request)
	return redirect('landing')



