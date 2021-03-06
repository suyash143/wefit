# Generated by Django 3.1.3 on 2021-02-10 11:00

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dietitian', '0002_auto_20210210_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='information',
            name='back_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Bimage'),
        ),
        migrations.AddField(
            model_name='information',
            name='front_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Fimage'),
        ),
        migrations.AddField(
            model_name='information',
            name='left_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Limage'),
        ),
        migrations.AddField(
            model_name='information',
            name='payment_screenshot',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='screenshot'),
        ),
        migrations.AddField(
            model_name='information',
            name='right_profile',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='Rimage'),
        ),
    ]
