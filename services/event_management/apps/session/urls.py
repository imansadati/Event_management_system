from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import SessionEventGetwayApiViewSet


router = DefaultRouter()

# sessions with event_id
session_event_list = SessionEventGetwayApiViewSet.as_view({
    'post': 'create',
    'get': 'list'
})


urlpatterns = [
    # sessions with event_id
    path('events/<int:event_id>/sessions',
         session_event_list, name='session_event_list'),

    # root
    path('', include(router.urls)),
]
