# Generated by Django 3.1.3 on 2021-02-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0007_information_weight_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='type_of_plan',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]