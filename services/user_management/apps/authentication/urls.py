from django.urls import path
from .apis import (AttendeeRegisterApi, LoginApi, CustomRefreshTokenApi,
                   LogoutApi, ChangePasswordApi, ForgotPasswordApi,
                   ResetPasswordApi, InviteUserViaAdminApi, AcceptInviteViaAdminApi)

urlpatterns = [
    path('signup/', AttendeeRegisterApi.as_view(), name='attendee_register'),
    path('signin/', LoginApi.as_view(), name='login'),
    path('refresh/', CustomRefreshTokenApi.as_view(), name='refresh'),
    path('logout/', LogoutApi.as_view(), name='logout'),
    path('change-password/', ChangePasswordApi.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordApi.as_view(), name='forgot_password'),
    path('reset-password', ResetPasswordApi.as_view(), name='reset_password'),
    path('invite-user/', InviteUserViaAdminApi.as_view(), name='invite_user'),
    path('accept-invite', AcceptInviteViaAdminApi.as_view(), name='accept_invite'),
]
