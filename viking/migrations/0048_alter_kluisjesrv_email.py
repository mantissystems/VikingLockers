# Generated by Django 4.1 on 2023-04-21 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viking', '0047_remove_kluisjesrv_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kluisjesrv',
            name='email',
            field=models.CharField(max_length=200),
        ),
    ]