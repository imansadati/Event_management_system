from django.urls import path
from .apis import AttendeeRegisterApi, AttendeeLoginApi

urlpatterns = [
    path('signup/', AttendeeRegisterApi.as_view(), name='attendee_register'),
    path('signin/', AttendeeLoginApi.as_view(), name='attendee_login'),
]
