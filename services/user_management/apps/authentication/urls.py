from django.urls import path
from .apis import AttendeeSignupApi

urlpatterns = [
    path('signup/', AttendeeSignupApi.as_view(), name='attendee_signup'),
]
