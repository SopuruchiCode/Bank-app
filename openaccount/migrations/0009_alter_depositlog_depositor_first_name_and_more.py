# Generated by Django 4.2 on 2024-07-23 16:04

from django.db import migrations, models
import openaccount.models


class Migration(migrations.Migration):

    dependencies = [
        ('openaccount', '0008_alter_depositlog_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositlog',
            name='depositor_first_name',
            field=models.CharField(max_length=50, validators=[openaccount.models.min_name_length]),
        ),
        migrations.AlterField(
            model_name='depositlog',
            name='depositor_last_name',
            field=models.CharField(max_length=50, validators=[openaccount.models.min_name_length]),
        ),
    ]
