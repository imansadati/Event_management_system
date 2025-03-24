from django.urls import path
from .apis import AttendeeRegisterApi, LoginApi, CustomRefreshTokenApi

urlpatterns = [
    path('signup/', AttendeeRegisterApi.as_view(), name='attendee_register'),
    path('signin/', LoginApi.as_view(), name='login'),
    path('refresh/', CustomRefreshTokenApi.as_view(), name='refresh'),
]
