from django.db import models
from django.contrib.auth.models import User
from ta.models import Testing_Activity
from datetime import datetime

class TestingRequest(models.Model):
	
	# requester = models.OneToOneField(User) 
	# requester = models.ManyToManyField(User,primary_key=True)
	requester = models.CharField(max_length=128, blank=True, null=True)
	responser = models.CharField(max_length=128, blank=True, null=True)
	# date = models.DateField()
	date = models.DateTimeField(auto_now_add=True)
	date_action = models.DateTimeField(auto_now = True)
	item = models.ManyToManyField(Testing_Activity) #Should be items
	email = models.EmailField()
	comment = models.TextField()

	status = models.CharField(max_length=20, default='Waiting List')

	def __unicode__(self):
		return '%s: %s @ %s' % (self.requester, self.item, self.date)

	def requester_count(self, keyword):
		return self.filter(requester__icontains=keyword).count()

	def date_count(self, keyword):
		return self.filter(date__icontains=keyword).count()

	def item_count(self, keyword):
		return self.filter(item__icontains=keyword).count()

	def status_count(self, keyword):
		return self.filter(status__icontains=keyword).count

	# uploadfile = models.FileField()
	# 
# Create your models here.