# Generated by Django 4.2.3 on 2023-07-27 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hashtags',
        ),
    ]
