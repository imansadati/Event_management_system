import grpc
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from grpc_service.client.generated import user_pb2
from grpc_service.client.generated.user_pb2_grpc import UserServiceStub
from grpc_service.client.generated import notification_pb2
from grpc_service.client.generated.notification_pb2_grpc import NotificationServiceStub
from grpc_service.client.generated import user_with_role_pb2
from grpc_service.client.generated.user_with_role_pb2_grpc import UserServiceViaRoleStub


def validate_user_exists(user_id):
    try:
        with grpc.insecure_channel('user_management:50052') as channel:
            stub = UserServiceStub(channel)
            response = stub.GetUser(user_pb2.GetUserRequest(
                id=user_id
            ))
            return response

    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise ValidationError('User not found')
        else:
            raise ValidationError(f'gRPC error: {e.details()}')


def send_email_via_rpc(recipient, subject, body):
    with grpc.insecure_channel("notification:50051") as channel:
        stub = NotificationServiceStub(channel)
        response = stub.SendEmail(notification_pb2.SendEmailRequest(
            recipient=recipient,
            subject=subject,
            body=body
        ))
        return response.success


class RemoteUser:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.email


class RemoteUserClient:
    """ Validate any type of user (admin, staff, attendee) with role. """

    @staticmethod
    def get_user(user_id, role):
        try:
            with grpc.insecure_channel('user_management:50052') as channel:
                stub = UserServiceViaRoleStub(channel)
                response = stub.GetUserViaRole(user_with_role_pb2.GetUserViaRoleRequest(
                    id=str(user_id),
                    role=role
                ))

            return RemoteUser(id=response.id, email=response.email, role=response.role)
            # return response

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise AuthenticationFailed(f"gRPC error: {e.details()}")
