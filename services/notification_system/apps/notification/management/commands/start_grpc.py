from pathlib import Path
from django.core.management.base import BaseCommand
import os
from django.conf import settings
import subprocess


class Command(BaseCommand):
    help = 'Compiles gRPC proto files and starts the gRPC server.'

    def handle(self, *args, **options):
        proto_path = Path(settings.BASE_DIR / 'grpc_service/server/proto')
        out_path = Path(settings.BASE_DIR / 'grpc_service/server/generated')

        os.makedirs(out_path, exist_ok=True)

        subprocess.run([
            'python', '-m', 'grpc_tools.protoc',
            f'--proto_path={proto_path}',
            f'--python_out={out_path}',
            f'--grpc_python_out={out_path}',
            os.path.join(proto_path, 'notification.proto')
        ], check=True)

        self.stdout.write(self.style.SUCCESS('Proto files compiled.'))

        # Fix import format in generated files by grpc.
        # check it without this piece of code if worked for you, you can remove it.
        grpc_file = out_path / 'notification_pb2_grpc.py'
        if grpc_file.exists():
            with open(grpc_file, 'r') as f:
                content = f.read()
            content = content.replace(
                'import notification_pb2 as notification__pb2',
                'from . import notification_pb2 as notification__pb2'
            )
            with open(grpc_file, 'w') as f:
                f.write(content)

        from grpc_service.server.server import serve
        serve()
