# Generated by Django 4.2.3 on 2023-07-29 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_accountuser_email_alter_accountuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]