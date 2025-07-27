from generated.user_pb2_grpc import UserServiceServicer
from apps.users.models import AttendeeUser
import grpc
from grpc_service.server.generated import user_pb2
from concurrent import futures
from grpc_service.server.generated.user_pb2_grpc import add_UserServiceServicer_to_server


class UserService(UserServiceServicer):
    def GetUser(self, request, context):
        try:
            user = AttendeeUser.objects.get(id=request.user_id)
            return user_pb2.UserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
            )
        except AttendeeUser.DoesNotExist:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()


def serve():
    port = '50052'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(
        UserService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print('User gRPC Server started on port ' + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
