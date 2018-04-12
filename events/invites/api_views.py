from __future__ import unicode_literals

from django.shortcuts import render

from invites.models import Event, Person, Invite, Relationship
from django.contrib.auth.models import User
from invites.serializers import EventSerializer, PersonSerializer, InviteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework import (
    viewsets, permissions, status, pagination, filters
)

class UserViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	permission_classes = (permissions.AllowAny,)
	serializer_class = PersonSerializer

	@detail_route(methods=['post'], permission_classes=(permissions.AllowAny,))
	def add_friend(self, request, *args, **kwargs):
		owner = self.get_object()

		try:
			target_pk = request.data.get('friend')
			target = Person.objects.get(pk=target_pk)
			if target not in owner.friends.all():
				relationship = Relationship.objects.create(owner=owner, target=target)
			else:
				relationship = Relationship.objects.get(owner=owner, target=target)
		except:
			return Response("Please Provide The ID of a Requested Friend That is not already a Friend")
		return Response("Friends with" + str(relationship))
	
	@detail_route(methods=['post'], permission_classes=(permissions.AllowAny,))
	def create_authenticated(self, request, *args, **kwargs):
		return Response(status=status.HTTP_200_OK)

class InviteViewSet(viewsets.ModelViewSet):
	queryset = Invite.objects.all()
	permission_classes = (permissions.AllowAny,)
	serializer_class = InviteSerializer

class EventViewSet(viewsets.ModelViewSet):
	queryset = Event.objects.filter(privacy='PUBLIC')
	permission_classes = (permissions.AllowAny,)
	serializer_class = EventSerializer

	@detail_route(methods=['post'], permission_classes=(permissions.AllowAny,))
	def create_invite(self, request, *args, **kwargs):
		event = self.get_object()
		try:
			invitee_pk = request.data.get('invite')
			invitee = Person.objects.get(pk=invitee_pk)
			invite = Invite.objects.create(event=event, attendee=invitee, in_network=True)
			invite.save()
		except:	
			pass
		return Response(status=status.HTTP_200_OK)

	@detail_route(methods=['post'], permission_classes=(permissions.AllowAny,))
	def create_oon_invite(self, request, *args, **kwargs):
		event = self.get_object()
		name = request.data['name']
		phone = request.data['phone']
		invite = Invite.objects.create(backup_name=name, backup_phone=phone, event=event, in_network=False)
		invite.save()
		return Response(status=status.HTTP_200_OK)
