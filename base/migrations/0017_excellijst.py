# Generated by Django 4.1 on 2023-09-02 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_remove_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Excellijst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kluisnummer', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('--', '--'), ('H', 'hang'), ('C', 'cijfer')], default='--', max_length=18)),
                ('sleutels', models.CharField(default='----', max_length=18)),
                ('code', models.CharField(default='----', max_length=18)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['kluisnummer'],
            },
        ),
    ]