# Generated by Django 4.2.1 on 2023-05-22 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spray_backend', '0004_alter_person_gym_alter_person_profile_image_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
