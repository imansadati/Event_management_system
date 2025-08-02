from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import EventGetwayApiViewSet, EventCategoryGetwayApiViewSet, EventGuestGetwayApiViewSet, EventInviteGetwayApiViewSet

router = DefaultRouter()
router.register('events', EventGetwayApiViewSet, basename='event')

# category
category_list = EventCategoryGetwayApiViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
category_detail = EventCategoryGetwayApiViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'delete',
})

# guest list
guest_list = EventGuestGetwayApiViewSet.as_view({
    'post': 'create',
    'get': 'list',
})
guest_detail = EventGuestGetwayApiViewSet.as_view({
    'delete': 'delete',
})

# invite
invite_list = EventInviteGetwayApiViewSet.as_view({
    'post': 'create',
    'get': 'list',
})

urlpatterns = [
    # category
    path('events/categories/', category_list, name='event_category_list'),
    path('events/categories/<int:pk>/', category_detail,
         name='event_category_detail'),

    # guest list
    path('events/<int:event_id>/guest-list',
         guest_list, name='event_guest_list'),
    path('events/<int:event_id>/guest-list/<int:guest_id>',
         guest_detail, name='event_guest_detail'),

    # invite
    path('events/<int:event_id>/invites',
         invite_list, name='event_invite_list'),

    # root
    path('', include(router.urls)),
]
