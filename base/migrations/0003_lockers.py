# Generated by Django 4.1 on 2023-06-03 08:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_kluisjesrv_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lockers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kluisnummer', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('kluisje', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('--', '--'), ('H', 'hang'), ('C', 'cijfer')], default='--', max_length=18)),
                ('topic', models.CharField(default='----', max_length=18)),
                ('row', models.CharField(default='----', max_length=18)),
                ('col', models.CharField(default='----', max_length=18)),
                ('verhuurd', models.BooleanField(default=False)),
                ('owners', models.ManyToManyField(blank=True, related_name='owners', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['kluisnummer'],
            },
        ),
    ]