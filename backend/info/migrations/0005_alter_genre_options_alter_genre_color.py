# Generated by Django 4.1.3 on 2023-01-09 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('id',), 'verbose_name': 'Gemre', 'verbose_name_plural': 'Genres'},
        ),
        migrations.AlterField(
            model_name='genre',
            name='color',
            field=models.CharField(max_length=7, verbose_name='color'),
        ),
    ]
