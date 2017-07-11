from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from .validators import ASCIIUsernameValidator, UnicodeUsernameValidator
import re
from urllib.parse import urlparse

# Create your models here.

class CustomUser(AbstractUser):
	photo = models.ImageField(_('Photo'),upload_to='media', blank=True)

	def __init__(self, *args, **kwargs):
		self._meta.get_field('email').blank = False
		self._meta.get_field('email')._unique = True
		self._meta.get_field('username').validators = [UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()]
		self._meta.get_field('username').help_text = "Required. 30 characters or fewer. Letters, digits and ./+/-/_ only."
		super(CustomUser, self).__init__(*args, **kwargs)


	def clean(self, *args, **kwargs):
		super(CustomUser, self).clean()
		
	def save(self, *args, **kwargs):
		self.full_clean()
		user = super(CustomUser, self).save()
		return user

	def get_absolute_url(self):
		return "/%s/" % self.username
	
	def get_home_url(self):
		return reverse(settings.HOME_URL[self.type])




