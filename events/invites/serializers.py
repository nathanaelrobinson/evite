from rest_framework import serializers
from invites.models import Event, Person, Invite
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User

class PersonSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source="user.username", required=False)
	friends = serializers.StringRelatedField(many=True, read_only=True)
	class Meta:
		model = Person
		fields = ('id', 'phone','friends','name', 'username')
		extra_kwargs = {'username': {'write_only': True, 'required': False}}
	
	def create(self, validated_data):
		_user = validated_data.pop('user', None)
		_friends = validated_data.pop('friends', None)
		username = _user['username']
		user = User.objects.create(username=username)
		user.save()
		person = Person.objects.create(user=user, **validated_data)
		person.save()
		return person
	def update(self, instance, validated_data):
		person = Person.objects.get(pk=instance.id)
		user = person.user
		old_username = user.username
		_user = validated_data.pop('user', None)
		username = _user['username']
		if old_username != username and username != None:
			user.username = username
			user.save()
		for item, key in validated_data.items():
			setattr(person, item, key)
		person.save()
		return person



class Person4InviteSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Person
		fields = ('id', 'phone', 'name')

class InviteSerializer(serializers.ModelSerializer):
	attendee = Person4InviteSerializer(many=False)
	event = serializers.CharField(source='event.name', required=False, read_only=True)
	class Meta:
		model = Invite
		fields = ('id', 'event', 'status', 'attendee')

class InvitedPersonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Invite
		fields =('id','status','name', 'phone')

class EventSerializer(serializers.ModelSerializer):
	invites = InvitedPersonSerializer(many=True, read_only=True)
	class Meta:
		model = Event
		fields = ('id', 'name', 'date', 'address', 'details', 'privacy', 'category', 'invites')