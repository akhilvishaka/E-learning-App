# Generated by Django 3.0.6 on 2020-07-22 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200623_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='stages',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
