from django.urls import path
from .apis import AdminUserListApi, StaffUserListApi, AttendeeUserListApi

urlpatterns = [
    path('admins/', AdminUserListApi.as_view(), name='admin_user_list'),
    path('staff/', StaffUserListApi.as_view(), name='staff_user_list'),
    path('attendees/', AttendeeUserListApi.as_view(), name='staff_attendee_list'),
]
