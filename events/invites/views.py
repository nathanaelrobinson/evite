# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from invites.models import Event, Attendee, Organizer
from invites.serializers import EventSerializer, AttendeeSerializer, OrganizerSerializer
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