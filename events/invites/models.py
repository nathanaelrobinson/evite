# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Event(models.Model):
	PRIVATE = "PRIVATE"
	PUBLIC = "PUBLIC"
	SEMI_PUBLIC = "SEMI_PUBLIC"
	privacy_choices = (
		(PRIVATE, "Private"),
		(PUBLIC, "Public"),
		(SEMI_PUBLIC, "Semi_Public"),
	)

	name = models.CharField(max_length=100, blank=True)
	date = models.DateTimeField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	address = models.CharField(max_length=400, null=True, blank=True)
	details = models.TextField(null=True, blank=True)
	privacy = models.CharField(choices=privacy_choices, max_length=20, default=PRIVATE, null=True, blank=True)
	category = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Attendee(models.Model):
	RSVP_YES = "Yes"
	RSVP_NO = "No"
	RSVP_YES_ANON = "Yes Anon"
	RSVP_MAYBE = "Maybe"
	RSVP_TBD = "TBD"
	rsvp_choices = (
		(RSVP_YES, "Attending"),
		(RSVP_NO, "Not Attending"),
		(RSVP_YES_ANON, "Attending Anonymously"),
		(RSVP_MAYBE, "Maybe Attending"),
		(RSVP_TBD, "Unresponded"),
	)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	status = models.CharField(choices=rsvp_choices, max_length=10, default=RSVP_TBD)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name + ": " + self.status

@python_2_unicode_compatible
class Organizer(models.Model):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	
	user = models.OneToOneField(User)
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	friends = models.ManyToManyField("self", blank=True)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name
