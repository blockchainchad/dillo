# Generated by Django 2.2.14 on 2021-03-22 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0048_static_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_pinned_by_moderator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_pinned_by_moderator',
            field=models.BooleanField(default=False),
        ),
    ]