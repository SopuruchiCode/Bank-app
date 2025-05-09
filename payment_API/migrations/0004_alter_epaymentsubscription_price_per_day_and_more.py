# Generated by Django 4.2 on 2024-09-12 08:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_API', '0003_alter_epaymentsubscription_price_per_day_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epaymentsubscription',
            name='price_per_day',
            field=models.DecimalField(decimal_places=2, default=200.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='epaymentsubscription',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
