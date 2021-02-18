# Generated by Django 2.2.14 on 2021-02-15 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0044_post_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='hash_id',
            field=models.CharField(max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]