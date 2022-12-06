# Generated by Django 4.1.3 on 2022-12-02 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0007_alter_band_is_full_alter_band_is_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='band',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='request',
            name='creator',
        ),
        migrations.AddField(
            model_name='band',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='band_author', to=settings.AUTH_USER_MODEL, verbose_name='author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author_request', to=settings.AUTH_USER_MODEL, verbose_name='author'),
            preserve_default=False,
        ),
    ]