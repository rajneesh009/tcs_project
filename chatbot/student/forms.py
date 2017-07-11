from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from user.models import CustomUser
from student.models import Student
from urllib.parse import urlparse
import re
from material import *

class StudentLoginForm(forms.Form):
	username = forms.CharField(label=_('Username'), max_length=20, widget=forms.TextInput(attrs={'placeholder': _('Enter your username'), 'auto_focus':''}))
	password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder':_('Enter password')}))

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(StudentLoginForm, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		super(StudentLoginForm, self).clean(*args, **kwargs)
		username = self.cleaned_data.get('username', None)
		password = self.cleaned_data.get('password', None)
		if username and password:
			queryset = CustomUser.objects.filter(is_superuser=False)
			try:
				user = queryset.get(username=username)
			except CustomUser.DoesNotExist:
				raise forms.ValidationError(_('Invalid username'))
			self.user_cache = authenticate(username=username, password=password)
			if self.user_cache is None:
				raise forms.ValidationError(_('Invalid username or password'))
		return self.cleaned_data
	
	def get_user(self):
		return self.user_cache

class StudentSignupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(StudentSignupForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['username'].widget.attrs['maxlength'] = 20
		self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
		self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
	
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Enter password')}))
	password2 = forms.CharField(label=_('Re-enter Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password')}))

	def clean_username(self):
		username = self.cleaned_data.get('username', None)
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if email:
			domain = '.'.join(email.split('@')[-1].split('.')[:-1]).lower()
			for blacklisted in settings.DISALLOWED_EMAIL_DOMAINS: # Because a few of these provide subdomains. FOOBAR.domainname.com
				if blacklisted in domain:
					raise forms.ValidationError(_('This email domain is not allowed. Please enter email of different domain.'))
		return email

	def clean(self, *args, **kwargs):
		super(StudentSignupForm, self).clean(*args, **kwargs)
		pwd1 = self.cleaned_data.get('password1', None)
		pwd2 = self.cleaned_data.get('password2', None)
		if pwd1 and pwd2:
			if pwd1 != pwd2:
				raise forms.ValidationError(_('Passwords must match.'))
			password_validation.validate_password(pwd1)
		return self.cleaned_data

	def save(self, commit=True, *args, **kwargs):
		student = super(StudentSignupForm, self).save(commit=False)
		student.set_password(self.cleaned_data['password2'])
		if commit:
			try:
				student.save()
			except IntegrityError:
				raise forms.ValidationError(_('Student already exists'))
			except ValidationError as error:
				raise forms.ValidationError(error)
		return student

	class Meta:
		model = CustomUser
		fields = ['username', 'email']
		labels = {'username': _('Enrollment Number')}
		help_texts = {
			'username': _('This should be unique and will be used for logging in'),
			'email': _('You\'ll need to verify this email address. Make sure you have access to it.'),
		}


