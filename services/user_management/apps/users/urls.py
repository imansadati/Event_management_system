from django.urls import path
from .apis import AdminUserListApi, StaffUserListApi

urlpatterns = [
    path('admins/', AdminUserListApi.as_view(), name='admin_user_list'),
    path('staff/', StaffUserListApi.as_view(), name='staff_user_list'),
]
