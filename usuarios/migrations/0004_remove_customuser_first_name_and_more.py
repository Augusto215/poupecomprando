# Generated by Django 5.0 on 2023-12-13 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_remove_customuser_email_verification_token_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='pontos',
        ),
    ]
