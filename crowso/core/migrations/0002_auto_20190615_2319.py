# Generated by Django 2.2.1 on 2019-06-15 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.IntegerField(choices=[(1, 'translate'), (2, 'type'), (3, 'other')]),
        ),
    ]
