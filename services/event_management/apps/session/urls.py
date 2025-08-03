from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import SessionEventGetwayApiViewSet, SessionGetwayApiViewSet


router = DefaultRouter()

# sessions with event_id
session_event_list = SessionEventGetwayApiViewSet.as_view({
    'post': 'create',
    'get': 'list'
})

# sessions
session_detail = SessionGetwayApiViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

urlpatterns = [
    # sessions with event_id
    path('events/<int:event_id>/sessions',
         session_event_list, name='session_event_list'),

    # sessions
    path('sessions/<int:session_id>', session_detail, name='session_detail'),

    # root
    path('', include(router.urls)),
]
