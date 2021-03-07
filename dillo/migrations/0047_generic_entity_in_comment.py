# Generated by Django 2.2.14 on 2021-03-03 00:09
import sys

from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    """Set published_at date matching latest update."""
    # Detect if tests are running
    if 'test' in sys.argv:
        return

    Comment = apps.get_model('dillo', 'Comment')
    db_alias = schema_editor.connection.alias
    post_type = ContentType.objects.get(app_label='dillo', model='post')
    for comment in Comment.objects.using(db_alias):
        comment.entity_object_id = comment.post.id
        comment.entity_content_type_id = post_type.id
        comment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dillo', '0046_post_is_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='entity_content_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.ContentType',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='entity_object_id',
            field=models.PositiveIntegerField(null=True),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
        migrations.RemoveField(model_name='comment', name='post',),
    ]
