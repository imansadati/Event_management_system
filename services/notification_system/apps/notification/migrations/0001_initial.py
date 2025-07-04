# Generated by Django 5.1.4 on 2025-04-04 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=256)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('error_message', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
