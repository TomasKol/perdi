# Generated by Django 3.0.3 on 2020-05-19 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0005_translation_language'),
        ('accounts', '0002_auto_20200519_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='current_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entries.Language'),
        ),
    ]
