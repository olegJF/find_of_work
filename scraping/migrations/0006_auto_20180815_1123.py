# Generated by Django 2.0.7 on 2018-08-15 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0005_error'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='error',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Ошибки скрапинга', 'verbose_name_plural': 'Ошибки скрапинга'},
        ),
        migrations.AddField(
            model_name='city',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='specialty',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
