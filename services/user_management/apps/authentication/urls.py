from django.urls import path
from .apis import AttendeeRegisterApi, LoginApi, CustomRefreshTokenApi, LogoutApi, ChangePasswordApi, ForgotPasswordApi

urlpatterns = [
    path('signup/', AttendeeRegisterApi.as_view(), name='attendee_register'),
    path('signin/', LoginApi.as_view(), name='login'),
    path('refresh/', CustomRefreshTokenApi.as_view(), name='refresh'),
    path('logout/', LogoutApi.as_view(), name='logout'),
    path('change-password/', ChangePasswordApi.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordApi.as_view(), name='forgot_password'),
]
