# Generated by Django 4.1.3 on 2023-01-09 18:49

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_alter_instrument_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=[('#FFFFFF', 'white'), ('#000000', 'black')])),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Gemre',
                'verbose_name_plural': 'Genres',
                'ordering': ('title',),
            },
        ),
    ]
