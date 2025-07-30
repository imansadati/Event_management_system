from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import EventGetwayApiViewSet, EventCategoryGetwayApiViewSet, EventGuestGetwayApiViewSet

router = DefaultRouter()
router.register('events', EventGetwayApiViewSet, basename='event')

urlpatterns = [
    path('events/categories/',
         EventCategoryGetwayApiViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('events/categories/<int:pk>/', EventCategoryGetwayApiViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'delete',
    })),
    path('events/<int:event_id>/guest-list', EventGuestGetwayApiViewSet.as_view({
        'post': 'create',
    })),
    path('', include(router.urls)),
]
