# Generated by Django 2.1.7 on 2019-07-07 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_contributor',
        ),
    ]