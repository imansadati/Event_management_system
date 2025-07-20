from rest_framework.routers import DefaultRouter
from .apis import OrganizerGetwayApiViewset, OrganizerMemberGetwayApiViewset
from django.urls import path, include


router = DefaultRouter()
router.register('organizers', OrganizerGetwayApiViewset, basename='organizer')

urlpatterns = [
    path('organizers/members/',
         OrganizerMemberGetwayApiViewset.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
