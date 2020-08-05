# Generated by Django 2.2.11 on 2020-08-05 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dillo', '0027_post_is_hidden_by_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField()),
                ('tagline', models.TextField()),
                ('description', models.TextField()),
                ('visibility', models.CharField(choices=[('public', 'Public'), ('unlisted', 'Unlisted'), ('private', 'Private')], default='unlisted', max_length=20)),
                ('is_featured', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dillo.Community'),
        ),
    ]