# Generated by Django 3.1.3 on 2021-02-13 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_info_is_dietitian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='is_dietitian',
            field=models.BooleanField(default=False),
        ),
    ]
