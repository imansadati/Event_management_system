from grpc_service.server.generated.user_pb2_grpc import UserServiceServicer
from grpc_service.server.generated.user_with_role_pb2_grpc import UserServiceViaRoleServicer
from apps.users.models import AttendeeUser
import grpc
from grpc_service.server.generated import user_pb2
from concurrent import futures
from grpc_service.server.generated.user_pb2_grpc import add_UserServiceServicer_to_server
from grpc_service.server.generated.user_with_role_pb2_grpc import add_UserServiceViaRoleServicer_to_server
from apps.users.models import AdminUser, StaffUser, AttendeeUser
from grpc_service.server.generated import user_with_role_pb2


ROLE_MODEL_MAP = {
    'attendee': AttendeeUser,
    'staff': StaffUser,
    'admin': AdminUser,
}


class UserService(UserServiceServicer):
    def GetUser(self, request, context):
        try:
            user = AttendeeUser.objects.get(id=str(request.id))
            return user_pb2.GetUserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
            )
        except AttendeeUser.DoesNotExist:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.GetUserResponse()


class UserServiceViaRole(UserServiceViaRoleServicer):
    def GetUser(self, request, context):
        try:
            user_id = request.user_id
            role = request.role

            if not role or role not in ROLE_MODEL_MAP:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                              'Invalid or missing role')

            model = ROLE_MODEL_MAP[role]
            user = model.objects.filter(id=user_id).first()

            if not user:
                context.abort(grpc.StatusCode.NOT_FOUND, 'User not found')

            return user_with_role_pb2.GetUserResponse(
                id=str(user.id),
                email=user.email,
                role=role
            )

        except Exception as e:
            context.abort(grpc.StatusCode.ABORTED, e)


def serve():
    port = '50052'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserService(), server)
    add_UserServiceViaRoleServicer_to_server(UserServiceViaRole(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print('User gRPC Server started on port ' + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
