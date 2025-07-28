import grpc
from grpc_service.client.generated.user_pb2_grpc import UserServiceStub
from grpc_service.client.generated import user_pb2
from rest_framework.exceptions import ValidationError


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
