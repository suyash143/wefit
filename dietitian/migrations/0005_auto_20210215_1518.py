# Generated by Django 3.1.3 on 2021-02-15 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0004_auto_20210215_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='attachment',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
