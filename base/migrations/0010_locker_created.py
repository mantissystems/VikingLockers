# Generated by Django 4.1 on 2023-07-09 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_user_locker'),
    ]

    operations = [
        migrations.AddField(
            model_name='locker',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 9, 15, 48, 28, 451381, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]