# Generated by Django 4.2.1 on 2023-06-06 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spray_backend', '0014_circuit_color_circuit_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuit',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
