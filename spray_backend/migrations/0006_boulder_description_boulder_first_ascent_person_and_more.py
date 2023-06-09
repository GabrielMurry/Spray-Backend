# Generated by Django 4.2.1 on 2023-05-22 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spray_backend', '0005_alter_gym_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='boulder',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='boulder',
            name='first_ascent_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='first_ascent_person', to='spray_backend.person'),
        ),
        migrations.AddField(
            model_name='boulder',
            name='matching',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='boulder',
            name='publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='boulder',
            name='setter_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='setter_person', to='spray_backend.person'),
        ),
        migrations.AlterField(
            model_name='boulder',
            name='grade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='boulder',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='boulder',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='boulder',
            name='sends',
            field=models.IntegerField(default=0),
        ),
    ]
