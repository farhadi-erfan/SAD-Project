# Generated by Django 2.2.1 on 2019-06-15 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190615_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesterproject',
            name='project',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
            preserve_default=False,
        ),
    ]