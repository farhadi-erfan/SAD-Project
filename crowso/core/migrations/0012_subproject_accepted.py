# Generated by Django 2.2.1 on 2019-08-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190802_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproject',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
