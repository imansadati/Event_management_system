# Generated by Django 5.1.4 on 2025-03-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_adminuser_updated_at_attendeeuser_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffuser',
            name='availability_status',
            field=models.CharField(choices=[('available', 'Available'), ('busy', 'Busy')], default='available', max_length=32),
        ),
    ]
