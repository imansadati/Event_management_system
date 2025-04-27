import grpc
from grpc_service.client.generated.notification_pb2_grpc import NotificationServiceStub
from grpc_service.client.generated import notification_pb2


def send_email_via_rpc(recipient, subject, body):
    with grpc.insecure_channel("notification:50051") as channel:
        stub = NotificationServiceStub(channel)
        response = stub.SendEmail(notification_pb2.SendEmailRequest(
            recipient=recipient,
            subject=subject,
            body=body
        ))
        return response.success
