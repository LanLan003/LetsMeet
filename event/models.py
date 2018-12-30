from django.db import models

# Create your models here.
#from django.conf import settings
#from datetime import datetime

class Event(models.Model):
	eventName = models.CharField(max_length=64, blank=False)
	owner = models.CharField(max_length=32, blank=False)
	dayChosen = models.CharField(max_length=64, blank=False)
	timeChosen = models.CharField(max_length=256, blank=False)
	randUrl = models.CharField(max_length=20, blank=False, primary_key = True)

	def __str__(self):
		return self.eventName + ':' + self.dayChosen

class Response(models.Model):
	yourName = models.CharField(max_length=32, blank=False)
	freeTime = models.CharField(max_length=1024, blank=False)
	event = models.ForeignKey('Event', on_delete=models.CASCADE)

	def __str__(self):
		return self.yourName + ':' + self.freeTime