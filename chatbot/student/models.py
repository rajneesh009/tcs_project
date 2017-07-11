from django.core import validators
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from user.models import CustomUser
from urllib.parse import urlparse
from decimal import Decimal

# Create your models here.

class Student(models.Model):
	
# General Details
	profile = models.OneToOneField(CustomUser, related_name="student")
	firstname = models.CharField(_('First name'), max_length=128)
	lastname = models.CharField(_('Last name'), max_length=128, blank=True)
	photo = models.ImageField(_('Photo'),upload_to='media', blank=True)
	dob = models.DateField(_('Date Of Birth'), null=True, blank=True)
	
	def get_full_name(self):
		return (self.firstname + " " + self.lastname).title()

	def __str__(self):
		return self.get_full_name()
	
	def get_absolute_url(self):
		return "/user/%s/" % self.profile.username
