# Generated by Django 2.2.14 on 2021-04-05 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0054_entity_dillo_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staticasset',
            name='source_filename',
            field=models.CharField(blank=True, editable=False, max_length=256),
        ),
    ]
