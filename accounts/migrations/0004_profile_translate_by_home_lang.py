# Generated by Django 3.0.3 on 2020-05-21 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200519_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='translate_by_home_lang',
            field=models.BooleanField(default=False),
        ),
    ]
