from django.urls import path
from .apis import AdminUserListApi, StaffUserListApi, AttendeeUserListApi, AdminUserDetailApi, StaffUserDetailApi, AttendeeUserDetailApi

urlpatterns = [
    path('admins/', AdminUserListApi.as_view(), name='admin_user_list'),
    path('staff/', StaffUserListApi.as_view(), name='staff_user_list'),
    path('attendees/', AttendeeUserListApi.as_view(), name='attendee_user_list'),
    path('admin/<int:user_id>/', AdminUserDetailApi.as_view(),
         name='admin_user_detail'),
    path('staff/<int:user_id>/', StaffUserDetailApi.as_view(),
         name='staff_user_detail'),
    path('attendee/<int:user_id>/', AttendeeUserDetailApi.as_view(),
         name='attendee_user_detail'),
]
