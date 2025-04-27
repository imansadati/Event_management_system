import grpc
from concurrent import futures
from grpc_service.server.generated.notification_pb2_grpc import NotificationServiceServicer, add_NotificationServiceServicer_to_server
from grpc_service.server.generated import notification_pb2
from apps.notification.utils import send_email


class NotificationService(NotificationServiceServicer):
    def SendEmail(self, request, context):
        print(f'send email for: {request.recipient}')

        success = send_email(request.recipient, request.subject, request.body)
        if success:
            return notification_pb2.SendEmailResponse(success=True, message='Email sent')
        else:
            return notification_pb2.SendEmailResponse(success=False, message='Failed to sent')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_NotificationServiceServicer_to_server(
        NotificationService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print('Notification gRPC Server started on port ' + port)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
