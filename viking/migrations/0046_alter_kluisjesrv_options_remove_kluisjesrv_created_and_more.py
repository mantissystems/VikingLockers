# Generated by Django 4.1 on 2023-04-21 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viking', '0045_kluisjesrv'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kluisjesrv',
            options={},
        ),
        migrations.RemoveField(
            model_name='kluisjesrv',
            name='created',
        ),
        migrations.RemoveField(
            model_name='kluisjesrv',
            name='updated',
        ),
    ]