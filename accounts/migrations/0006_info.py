# Generated by Django 3.1.3 on 2020-12-16 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0005_auto_20201216_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('target', models.IntegerField(blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('profile', models.CharField(blank=True, max_length=400, null=True)),
                ('target_achieved', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
