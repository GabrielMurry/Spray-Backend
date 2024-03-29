# Generated by Django 4.2.1 on 2023-08-15 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spray_backend', '0023_remove_activity_message_activity_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='boulder',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='circuit',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='like',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='send',
            name='activity',
        ),
        migrations.AddField(
            model_name='activity',
            name='bookmark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spray_backend.bookmark'),
        ),
        migrations.AddField(
            model_name='activity',
            name='boulder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spray_backend.boulder'),
        ),
        migrations.AddField(
            model_name='activity',
            name='like',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spray_backend.like'),
        ),
        migrations.AddField(
            model_name='activity',
            name='send',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spray_backend.send'),
        ),
    ]
