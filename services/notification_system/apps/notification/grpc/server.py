import grpc
from concurrent import futures
import grpc.server
from proto import notification_pb2_grpc
from proto import notification_pb2


class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(
        NotificationService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
