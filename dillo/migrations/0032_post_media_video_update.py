# Generated by Django 2.2.11 on 2020-09-10 17:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0031_post_with_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmediavideo',
            name='source_metadata',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
