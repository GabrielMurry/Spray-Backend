# Generated by Django 4.2.1 on 2023-05-25 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spray_backend', '0010_rename_sends_boulder_sends_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='send',
            name='attempts',
        ),
        migrations.RemoveField(
            model_name='send',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='send',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='send',
            name='quality',
        ),
    ]
