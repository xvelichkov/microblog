# Generated by Django 4.2.3 on 2023-07-29 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_follower_unique_pair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='accountuser',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='accountuser',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
    ]
