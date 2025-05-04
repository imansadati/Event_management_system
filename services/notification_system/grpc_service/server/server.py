import grpc
from concurrent import futures
from grpc_service.server.generated.notification_pb2_grpc import NotificationServiceServicer, add_NotificationServiceServicer_to_server
from grpc_service.server.generated import notification_pb2
from apps.notification.tasks import send_email_task


class NotificationService(NotificationServiceServicer):
    def SendEmail(self, request, context):
        print(f'sending email for: {request.recipient} - {request.subject}')

        send_email_task.delay(
            request.recipient, request.subject, request.body)

        return notification_pb2.SendEmailResponse(
            success=True,
            message='Email queued successfully',
        )


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
