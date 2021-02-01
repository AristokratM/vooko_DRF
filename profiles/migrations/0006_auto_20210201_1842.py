# Generated by Django 3.1.5 on 2021-02-01 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('profiles', '0005_auto_20210201_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquaintancerequest',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'profiles'), ('model', 'friendsprofile')), models.Q(('app_label', 'profiles'), ('model', 'datesprofile')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='match',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'profiles'), ('model', 'friendsprofile')), models.Q(('app_label', 'profiles'), ('model', 'datesprofile')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
