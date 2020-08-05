# Generated by Django 2.2.2 on 2020-01-31 00:42

import dillo.models
from django.db import migrations, models

import dillo.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0004_add_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='event', name='image_height', field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='event', name='image_width', field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(
                blank=True,
                height_field='image_height',
                upload_to=dillo.models.mixins.get_upload_to_hashed_path,
                width_field='image_width',
            ),
        ),
    ]