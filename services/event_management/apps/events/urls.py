from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import EventGetwayApiViewSet, EventCategoryGetwayApiViewSet

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
    path('', include(router.urls)),
]
