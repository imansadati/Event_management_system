from django.urls import path
from .apis import AdminUserListApi

urlpatterns = [
    path('admins/', AdminUserListApi.as_view(), name='admin_user_list')
]
