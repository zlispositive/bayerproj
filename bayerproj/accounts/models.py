#coding=utf-8

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User, UserManager
from django.db import models

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	# name = models.CharField(max_length=30,blank=True,null=True)
	title = models.CharField(max_length = 100)
	bu = models.CharField(max_length = 100 )
	# email = models.EmailField(max_length=254)
	rank = models.CharField(max_length = 1, blank=True, null=True)

	class Meta:
		ordering=['rank']
	def __unicode__(self):
		return  "%s Level %s: %s, %s" % (self.bu, self.rank, self.user.username, self.title)