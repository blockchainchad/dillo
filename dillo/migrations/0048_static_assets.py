# Generated by Django 2.2.11 on 2021-03-14 17:03

import sys

from django.contrib.contenttypes.models import ContentType
import dillo.models.mixins
from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    """Set published_at date matching latest update."""
    # Detect if tests are running
    if 'test' in sys.argv:
        return
    post_media_image_type = ContentType.objects.get(app_label='dillo', model='postmediaimage')
    post_media_video_type = ContentType.objects.get(app_label='dillo', model='postmediavideo')

    StaticAsset = apps.get_model('dillo', 'StaticAsset')
    Image = apps.get_model('dillo', 'Image')
    Video = apps.get_model('dillo', 'Video')
    PostMedia = apps.get_model('dillo', 'PostMedia')
    PostMediaImage = apps.get_model('dillo', 'PostMediaImage')
    PostMediaVideo = apps.get_model('dillo', 'PostMediaVideo')
    db_alias = schema_editor.connection.alias
    for post_media in PostMedia.objects.using(db_alias):
        source_type = 'file'
        if post_media.content_type.id == post_media_image_type.id:
            post_media.content_object = PostMediaImage.objects.get(id=post_media.object_id)
            post_media.content_object.source = post_media.content_object.image
            source_type = 'image'
        else:
            post_media.content_object = PostMediaVideo.objects.get(id=post_media.object_id)

        static_asset = StaticAsset.objects.create(
            source=post_media.content_object.source,
            source_type=source_type,
            source_filename=post_media.content_object.source_filename,
        )

        if source_type == 'image':
            Image.objects.create(
                static_asset=static_asset,
                height=post_media.content_object.image.height,
                width=post_media.content_object.image.width,
            )
            static_asset.thumbnail = post_media.content_object.image

        if post_media.content_type.id == post_media_video_type.id:
            static_asset.source_type = 'video'
            static_asset.thumbnail = post_media.content_object.thumbnail
            static_asset.thumbnail_height = post_media.content_object.thumbnail_height
            static_asset.thumbnail_width = post_media.content_object.thumbnail_width
            Video.objects.create(
                static_asset=static_asset,
                framerate=post_media.content_object.framerate,
                aspect=post_media.content_object.aspect,
                encoding_job_id=post_media.content_object.encoding_job_id,
                encoding_job_status=post_media.content_object.encoding_job_status,
                views_count=post_media.content_object.views_count,
            )

        static_asset.hash_id = post_media.hash_id
        static_asset.save()
        post_media.post.media.add(static_asset)


class Migration(migrations.Migration):

    dependencies = [
        ('dillo', '0047_generic_entity_in_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticAsset',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('order', models.PositiveIntegerField(default=0)),
                (
                    'source',
                    models.FileField(
                        blank=True, upload_to=dillo.models.mixins.get_upload_to_hashed_path
                    ),
                ),
                (
                    'source_type',
                    models.CharField(
                        choices=[('file', 'File'), ('image', 'Image'), ('video', 'Video')],
                        default='file',
                        max_length=5,
                    ),
                ),
                ('source_filename', models.CharField(blank=True, editable=False, max_length=128)),
                ('size_bytes', models.BigIntegerField(editable=False, null=True)),
                ('hash_id', models.CharField(max_length=6, null=True, unique=True)),
                (
                    'thumbnail',
                    models.ImageField(
                        blank=True,
                        height_field='thumbnail_height',
                        upload_to='',
                        width_field='thumbnail_width',
                    ),
                ),
                ('thumbnail_height', models.PositiveIntegerField(blank=True, null=True)),
                ('thumbnail_width', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={'abstract': False,},
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('framerate', models.FloatField(null=True)),
                ('aspect', models.FloatField(null=True)),
                ('encoding_job_id', models.IntegerField(null=True)),
                ('encoding_job_status', models.CharField(max_length=128, null=True)),
                ('encoding_job_progress', models.CharField(blank=True, max_length=10, null=True)),
                ('views_count', models.PositiveIntegerField(default=0)),
                (
                    'static_asset',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to='dillo.StaticAsset'
                    ),
                ),
            ],
            options={'db_table': 'dillo_staticasset_video',},
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('height', models.PositiveIntegerField(blank=True, null=True)),
                ('width', models.PositiveIntegerField(blank=True, null=True)),
                (
                    'static_asset',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to='dillo.StaticAsset'
                    ),
                ),
            ],
            options={'db_table': 'dillo_staticasset_image',},
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.ManyToManyField(blank=True, related_name='post', to='dillo.StaticAsset'),
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
