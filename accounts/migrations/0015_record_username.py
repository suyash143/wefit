# Generated by Django 3.1.3 on 2020-12-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20201225_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
