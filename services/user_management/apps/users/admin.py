from django.contrib import admin
from .models import AdminUser, AttendeeUser, Profile, StaffUser


admin.site.register(AdminUser,)
admin.site.register(StaffUser,)
admin.site.register(AttendeeUser,)
admin.site.register(Profile,)
