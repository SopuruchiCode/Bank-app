# Generated by Django 4.2 on 2024-07-21 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openaccount', '0004_withdrawallog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawallog',
            name='coupon_code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
