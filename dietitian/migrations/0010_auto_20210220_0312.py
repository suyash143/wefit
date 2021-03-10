# Generated by Django 3.1.3 on 2021-02-19 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0009_information_end_of_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='unliked_food',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='information',
            name='wakeup_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]