# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from invites.models import Event, Person, Invite, Relationship
from invites.serializers import EventSerializer, PersonSerializer, InviteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, detail_route


class EventList(generics.ListCreateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = (permissions.AllowAny,)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = (permissions.AllowAny,)

class PersonList(generics.ListCreateAPIView):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer
	permission_classes = (permissions.AllowAny,)

class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer
	permission_classes = (permissions.AllowAny,)
	
	@detail_route(methods=['post'], permission_classes=(permissions.AllowAny))
	def add_friend(self, request, *args, **kwargs):
		print request
		owner = Person.objects.get(id=self.id)
		# target = Person.objects.get()
		return Response('Works')


class InviteList(generics.ListCreateAPIView):
	queryset = Invite.objects.all()
	serializer_class = InviteSerializer
	permission_classes = (permissions.AllowAny,)

class InviteDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Invite.objects.all()
	serializer_class = InviteSerializer
	permission_classes = (permissions.AllowAny,)





# class OrganizerList(generics.ListCreateAPIView):
# 	queryset = Organizer.objects.all()
# 	serializer_class = OrganizerSerializer
# 	permission_classes = (permissions.AllowAny,)

# class OrganizerDetail(generics.RetrieveUpdateDestroyAPIView):
# 	queryset = Organizer.objects.all()
# 	serializer_class = OrganizerSerializer
# 	permission_classes = (permissions.AllowAny,)