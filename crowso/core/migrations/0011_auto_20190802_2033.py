# Generated by Django 2.2.1 on 2019-08-02 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_is_contributor'),
        ('core', '0010_contributorsubproject_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='subprojects_num',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='contributorsubproject',
            name='sub_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to='core.SubProject'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='sub_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.SubProject'),
        ),
        migrations.AlterUniqueTogether(
            name='contributorsubproject',
            unique_together={('contributor', 'sub_project')},
        ),
    ]