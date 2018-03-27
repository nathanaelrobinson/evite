from rest_framework import serializers
from invites.models import Event, Attendee, Organizer
from rest_framework.decorators import api_view, permission_classes, detail_route


class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		fields = ('name', 'date', 'address', 'details', 'privacy', 'category')

class AttendeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attendee
		fields = ('event', 'status', 'user')

class OrganizerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organizer
		fields = ('user', 'phone_number')

