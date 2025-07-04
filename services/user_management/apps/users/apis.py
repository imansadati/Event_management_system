from rest_framework.views import APIView
from rest_framework import serializers, status
from .models import AdminUser, StaffUser, AttendeeUser
from django.http import HttpRequest, Http404
from .selectors import user_admin_list, user_staff_list, user_attendee_list, user_admin_get, user_staff_get, user_attendee_get
# read ./shared_utils/README.md
from shared_utils.pagination import LimitOffsetPagination, get_paginated_response
from shared_utils.permissions import IsAuthenticatedViaJWT, HasRolePermission
from rest_framework.response import Response
from .services import user_admin_create, user_staff_create, user_attendee_create, user_admin_update, user_staff_update, user_attendee_update
from rest_framework.exceptions import ValidationError


class AdminUserListApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class FilterSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        full_name = serializers.CharField(max_length=128, required=False)
        is_admin = serializers.BooleanField(
            allow_null=True, default=None, required=False)
        username = serializers.CharField(max_length=128, required=False)

    class OutputAdminSerializer(serializers.ModelSerializer):
        class Meta:
            model = AdminUser
            fields = '__all__'

    def get(self, request: HttpRequest):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_admin_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputAdminSerializer,
            queryset=users,
            request=request,
            view=self
        )


class StaffUserListApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class FilterSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        full_name = serializers.CharField(max_length=128, required=False)
        is_staff = serializers.BooleanField(
            allow_null=True, default=None, required=False)
        username = serializers.CharField(max_length=128, required=False)
        job_title = serializers.CharField(max_length=128, required=False)
        availability_status = serializers.CharField(
            max_length=128, required=False)

    class OutputStaffSerializer(serializers.ModelSerializer):
        class Meta:
            model = StaffUser
            fields = '__all__'

    def get(self, request: HttpRequest):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_staff_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputStaffSerializer,
            queryset=users,
            request=request,
            view=self
        )


class AttendeeUserListApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class Pagination(LimitOffsetPagination):
        default_limit = 2

    class FilterSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        full_name = serializers.CharField(max_length=128, required=False)
        is_attendee = serializers.BooleanField(
            allow_null=True, default=None, required=False)
        username = serializers.CharField(max_length=128, required=False)
        membership_status = serializers.CharField(
            max_length=128, required=False)

    class OutputAttendeeSerializer(serializers.ModelSerializer):
        class Meta:
            model = AttendeeUser
            fields = '__all__'

    def get(self, request: HttpRequest):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_attendee_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputAttendeeSerializer,
            queryset=users,
            request=request,
            view=self
        )


class AdminUserDetailApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class OutputAdminSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField(max_length=128)
        email = serializers.EmailField()
        is_admin = serializers.BooleanField()

    def get(self, request: HttpRequest, user_id):
        user = user_admin_get(user_id)

        data = self.OutputAdminSerializer(user).data

        return Response(data, status=status.HTTP_200_OK)


class StaffUserDetailApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class OutputStaffSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField(max_length=128)
        email = serializers.EmailField()
        availability_status = serializers.CharField(max_length=32)
        is_staff = serializers.BooleanField()

    def get(self, request: HttpRequest, user_id):
        user = user_staff_get(user_id)

        if user is None:
            raise Http404

        data = self.OutputStaffSerializer(user).data

        return Response(data, status=status.HTTP_200_OK)


class AttendeeUserDetailApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class OutputAttendeeSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        username = serializers.CharField(max_length=128)
        email = serializers.EmailField()
        is_attendee = serializers.BooleanField()

    def get(self, request: HttpRequest, user_id):
        user = user_attendee_get(user_id)

        data = self.OutputAttendeeSerializer(user).data

        return Response(data, status=status.HTTP_200_OK)


class AdminUserCreateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class InputAdminSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)
        full_name = serializers.CharField(max_length=128)
        username = serializers.CharField(max_length=128)

    def post(self, request: HttpRequest):
        serializer = self.InputAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_admin_create(**serializer.validated_data)

        data = AdminUserDetailApi.OutputAdminSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class StaffUserCreateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class InputStaffSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)
        full_name = serializers.CharField(max_length=128)
        username = serializers.CharField(max_length=128)
        job_title = serializers.CharField(max_length=128)
        work_experience = serializers.IntegerField()

    def post(self, request: HttpRequest):
        serializer = self.InputStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_staff_create(**serializer.validated_data)

        data = StaffUserDetailApi.OutputStaffSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class AttendeeUserCreateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class InputAttendeeSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)
        full_name = serializers.CharField(max_length=128)
        username = serializers.CharField(max_length=128)

    def post(self, request: HttpRequest):
        serializer = self.InputAttendeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_attendee_create(**serializer.validated_data)

        data = AttendeeUserDetailApi.OutputAttendeeSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class AdminUserUpdateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class InputAdminSerializer(serializers.Serializer):
        full_name = serializers.CharField(max_length=128)
        email = serializers.EmailField()

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def post(self, request: HttpRequest, user_id):
        serializer = self.InputAdminSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = user_admin_get(user_id)

        try:
            updated_user = user_admin_update(
                user=user, data=serializer.validated_data)

            return Response(AdminUserDetailApi.OutputAdminSerializer(updated_user).data, status=status.HTTP_200_OK)

        except ValidationError as e:
            if e.get_codes() == ["no_content"]:
                return Response({"detail": "No changes detected. User data remains the same."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class StaffUserUpdateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    class InputStaffSerializer(serializers.Serializer):
        full_name = serializers.CharField(max_length=128)
        email = serializers.EmailField()
        availability_status = serializers.ChoiceField(
            choices=[('available', 'Available'), ('busy', 'Busy')])

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def post(self, request: HttpRequest, user_id):
        serializer = self.InputStaffSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = user_staff_get(user_id)

        try:
            updated_user = user_staff_update(
                user=user, data=serializer.validated_data)

            return Response(StaffUserDetailApi.OutputStaffSerializer(updated_user).data, status=status.HTTP_200_OK)

        except ValidationError as e:
            if e.get_codes() == ["no_content"]:
                return Response({"detail": "No changes detected. User data remains the same."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class AttendeeUserUpdateApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    class InputAttendeeSerializer(serializers.Serializer):
        full_name = serializers.CharField(max_length=128)
        email = serializers.EmailField()

        # check the user does not enter additional fields
        def validate(self, data):
            extra_fields = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if extra_fields:
                raise ValidationError(
                    {"extra_fields": f"Unexpected fields: {', '.join(extra_fields)}"})
            return data

    def post(self, request: HttpRequest, user_id):
        serializer = self.InputAttendeeSerializer(
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = user_attendee_get(user_id)

        try:
            updated_user = user_attendee_update(
                user=user, data=serializer.validated_data)

            return Response(AttendeeUserDetailApi.OutputAttendeeSerializer(updated_user).data, status=status.HTTP_200_OK)

        except ValidationError as e:
            if e.get_codes() == ["no_content"]:
                return Response({"detail": "No changes detected. User data remains the same."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class AdminUserDeleteApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    def post(self, request: HttpRequest, user_id):
        user = user_admin_get(user_id)

        user.delete()

        return Response({'detail': f'This user with {user_id} id successfully deleted.'}, status=status.HTTP_200_OK)


class StaffUserDeleteApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin']

    def post(self, request: HttpRequest, user_id):
        user = user_staff_get(user_id)

        user.delete()

        return Response({'detail': f'This user with {user_id} id successfully deleted.'}, status=status.HTTP_200_OK)


class AttendeeUserDeleteApi(APIView):
    permission_classes = [IsAuthenticatedViaJWT, HasRolePermission]
    HasRolePermission.required_roles = ['admin', 'staff']

    def post(self, request: HttpRequest, user_id):
        user = user_attendee_get(user_id)

        user.delete()

        return Response({'detail': f'This user with {user_id} id successfully deleted.'}, status=status.HTTP_200_OK)
