# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.encoding import python_2_unicode_compatible

PRIVATE = "PRIVATE"
PUBLIC = "PUBLIC"
SEMI_PUBLIC = "SEMI_PUBLIC"
privacy_choices = (
	(PRIVATE, "Private"),
	(PUBLIC, "Public"),
	(SEMI_PUBLIC, "Semi_Public"),
)

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

@python_2_unicode_compatible
class Person(models.Model):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	
	user = models.OneToOneField(User)
	phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	name = models.TextField(max_length=100)
	friends = models.ManyToManyField("self", through="Relationship",through_fields=('owner','target'), symmetrical=False, null=True)

	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Event(models.Model):
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
class Invite(models.Model):
	in_network = models.BooleanField(default = False)
	#If the person is not in the network we'll initiate an unsubstantiated invite.
	backup_name = models.CharField(max_length=100, blank=True, null=True)
	backup_phone = models.CharField(max_length=17, blank=True, null=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invites", null=True)
	status = models.CharField(choices=rsvp_choices, max_length=10, default=RSVP_TBD)
	
	#If they are in the netowrk we will associate the invite to a person.
	attendee = models.ForeignKey(Person, null=True, blank=True, related_name="attendee")

	@property
	def name(self):
		#returns the name of the Invitee regardless if they are initiated or not.
		if self.in_network == False:
			return  self.backup_name
		return self.attendee.name
	def phone(self):
		if self.in_network == False:
			return self.backup_phone
		return self.attendee.phone

	def __str__(self):
		return self.name + ": " + self.status


@python_2_unicode_compatible
class Relationship(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="owner", null=True)
	target = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return "{} + {}".format(self.owner, self.target)




