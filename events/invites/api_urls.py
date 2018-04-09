from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from invites import views
from rest_framework import routers
from invites.api_views import InviteViewSet, UserViewSet, EventViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, 'User')
router.register(r'invites', InviteViewSet, 'Invite')
router.register(r'events', EventViewSet, 'Event')

urlpatterns = router.urls