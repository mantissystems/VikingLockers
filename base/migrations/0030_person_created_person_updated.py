# Generated by Django 4.1 on 2023-10-06 04:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_facturatielijst_obsolete'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.today),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]