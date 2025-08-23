from pathlib import Path
from django.core.management.base import BaseCommand
import os
from django.conf import settings
import subprocess


class Command(BaseCommand):
    help = 'Compiles all gRPC proto files and starts the gRPC server.'

    def handle(self, *args, **options):
        proto_path = Path(settings.BASE_DIR / 'grpc_service/server/proto')
        out_path = Path(settings.BASE_DIR / 'grpc_service/server/generated')

        os.makedirs(out_path, exist_ok=True)

        proto_files = list(proto_path.glob('*.proto'))

        if not proto_files:
            self.stdout.write(self.style.WARNING('No .proto files found.'))
            return

        for proto_file in proto_files:
            subprocess.run([
                'python', '-m', 'grpc_tools.protoc',
                f'--proto_path={proto_path}',
                f'--python_out={out_path}',
                f'--grpc_python_out={out_path}',
                str(proto_file)
            ], check=True)

        self.stdout.write(self.style.SUCCESS('All proto files compiled.'))

        # Auto-fix imports for each *_pb2_grpc.py
        for grpc_file in out_path.glob('*_pb2_grpc.py'):
            with open(grpc_file, 'r') as f:
                content = f.read()

            lines = content.splitlines()
            fixed_lines = []

            for line in lines:
                if line.startswith('import ') and '_pb2' in line:
                    # Example: import user_pb2 as user__pb2 → from . import user_pb2 as user__pb2
                    parts = line.split()
                    if len(parts) >= 4 and parts[1].endswith('_pb2'):
                        fixed_lines.append(
                            f"from . import {parts[1]} as {parts[3]}")
                    else:
                        fixed_lines.append(line)
                else:
                    fixed_lines.append(line)

            with open(grpc_file, 'w') as f:
                f.write('\n'.join(fixed_lines))

        self.stdout.write(self.style.SUCCESS(
            'Fixed relative imports in generated gRPC files.'))

        # Start the gRPC server (if needed)
        from grpc_service.server.server import serve
        serve()
