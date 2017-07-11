from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from user.models import CustomUser
from urllib.parse import urlparse
import re
from material import *

class LoginForm(forms.Form):
	username = forms.CharField(label=_('Username'), max_length=32, widget=forms.TextInput(attrs={'placeholder': _('or email address'), 'auto_focus':''}))
	password = forms.CharField(label=_('Password'), widget=forms.PasswordInput({'placeholder': _('Enter password')}))

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		super(LoginForm, self).clean()
		username = self.cleaned_data.get('username', None)
		password = self.cleaned_data.get('password', None)

		if username and password:
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

class SignupForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['username'].widget.attrs['placeholder'] = 'Enter a username'
		self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
	
	password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Enter password')}))
	password2 = forms.CharField(label=_('Re-enter Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm password')}))

	def clean(self, *args, **kwargs):
		super(SignupForm, self).clean(*args, **kwargs)
		pwd1 = self.cleaned_data.get('password1', None)
		pwd2 = self.cleaned_data.get('password2', None)
		if pwd1 and pwd2:
			if pwd1 != pwd2:
				raise forms.ValidationError(_('Passwords do not match.'))
			password_validation.validate_password(pwd1)
		return self.cleaned_data

	def clean_username(self):
		username = self.cleaned_data['username']
		'''
		if username and username in settings.DISALLOWED_USERNAMES:
			raise forms.ValidationError(_('You cannot take this username'))
		'''
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if email:
			domain = '.'.join(email.split('@')[-1].split('.')[:-1]).lower()
			for blacklisted in settings.DISALLOWED_EMAIL_DOMAINS: # Because a few of these provide subdomains. FOOBAR.domainname.com
				if blacklisted in domain:
					raise forms.ValidationError(_('This email domain is not allowed. Please enter email of different domain.'))
		return email

	def save(self, commit=True, *args, **kwargs):
		self.user_type = kwargs.pop('user_type')
		user = super(SignupForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get('password2'))
		user.is_active = True
		user.type = self.user_type
		if commit:
			try:
				user.save()
			except IntegrityError:
				raise forms.ValidationError(_('User already exists'))
			except ValidationError as error:
				raise forms.ValidationError(error)
		return user

	class Meta:
		model = CustomUser
		fields = ['username', 'email']
		help_texts = {
			'username': _('Required. 30 characters or fewer. Letters, digits and ./+/-/_ only.'),
			'email': _('You\'ll need to verify this email address. Make sure you have access to it.'),
		}




class AccountForm(forms.ModelForm):
	current_password = forms.CharField(label=_('Current Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Enter Current Password')}), required=False)
	new_password1 = forms.CharField(label=_('New Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Enter New Password')}), required=False)
	new_password2 = forms.CharField(label=_('Re-enter New Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm New Password')}), required=False)
	
	def __init__(self, *args, **kwargs):
		super(AccountForm, self).__init__(*args, **kwargs)
		self.password_changed = False
		self.fields['username'].widget.attrs['readonly'] = True
		self.fields['email'].widget.attrs['readonly'] = True
	
	def clean_current_password(self):
		current = self.cleaned_data.get('current_password', None)
		if current and not self.instance.check_password(current):
			raise forms.ValidationError(_('Please enter your existing password correctly'))
		return current
	
	def clean_username(self):
		data_username = self.cleaned_data.get('username', None)
		if data_username != self.instance.username:
			raise forms.ValidationError(_('Incorrect username'))
		return data_username
	
	def clean_email(self):
		data_email = self.cleaned_data.get('email', None)
		if data_email != self.instance.email:
			raise forms.ValidationError(_('Incorrect email'))
		return data_email
	
	def clean(self, *args, **kwargs):
		super(AccountForm, self).clean(*args, **kwargs)
		old = self.cleaned_data.get('current_password', None)
		new1 = self.cleaned_data.get('new_password1', None)
		new2 = self.cleaned_data.get('new_password2', None)
		if old:
			if not new1:
				raise forms.ValidationError(_('Please enter new password'))
			elif not new2:
				raise forms.ValidationError(_('Please confirm new password'))
			elif new1 != new2:
				raise forms.ValidationError(_('New passwords must match.'))
			elif new1 == old:
				raise forms.ValidationError(_('New password shouldn\'t be same as current one'))
			else:
				password_validation.validate_password(new2)
		else:
			if new1 or new2:
				raise forms.ValidationError(_('Please enter current password'))
		return self.cleaned_data
	
	def save(self, commit=True):
		user = super(AccountForm, self).save(commit=False)
		if self.cleaned_data.get('new_password2', None):
			user.set_password(self.cleaned_data['new_password2'])
			self.password_changed = True
		if commit:
			try:
				user.save()
			except IntegrityError:
				raise forms.ValidationError(_('Error Updating.'))
			except ValidationError as error:
				raise forms.ValidationError(error)
		return user

	class Meta:
		model = CustomUser
		fields = ['username', 'email']
		help_texts = {
			'username': 'Readonly. You cannot edit this field.',
			'email': 'Readonly. This field cannot be edited.',
		}

class ForgotPasswordForm(forms.Form):
	layout = Layout(
		Fieldset('Registration Details', Row('email'))
	)
	email = forms.EmailField(max_length = 254, help_text=_('Enter your registered email address'))
	def clean_email(self):
		data_email = self.cleaned_data.get('email', None)
		if not data_email:
			raise forms.ValidationError(_("Please enter an email-address."))
		return data_email

class SetPasswordForm(forms.Form):
	password1 = forms.CharField(label=_('Password'), widget = forms.PasswordInput)
	password2 = forms.CharField(label=_('Confirm Password'), widget = forms.PasswordInput, help_text = _('Enter same as above'))
	def clean_password2(self):
		data_password1 = self.cleaned_data.get('password1', None)
		data_password2 = self.cleaned_data.get('password2', None)
		if data_password1 and data_password2 and data_password1 != data_password2:
			raise forms.ValidationError(_("Passwords don't match"))
		if data_password1 and data_password2:
			password_validation.validate_password(data_password2)
		return data_password2
