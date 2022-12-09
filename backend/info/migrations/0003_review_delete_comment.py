# Generated by Django 4.1.3 on 2022-12-08 20:51

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('image', models.ImageField(default=None, null=True, upload_to='posts/images/', verbose_name='image')),
                ('audio', models.FileField(default=None, null=True, upload_to='posts/audios/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['wav', 'mp3'])], verbose_name='audio')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_reviews', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='info.post')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ('id',),
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
