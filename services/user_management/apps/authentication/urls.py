from django.urls import path
from .apis import AttendeeRegisterApi, LoginApi

urlpatterns = [
    path('signup/', AttendeeRegisterApi.as_view(), name='attendee_register'),
    path('signin/', LoginApi.as_view(), name='login'),
]
