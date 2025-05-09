# Generated by Django 4.2 on 2024-07-20 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depositor_first_name', models.CharField(max_length=50)),
                ('depositor_last_name', models.CharField(max_length=50)),
                ('account', models.CharField(max_length=8)),
                ('amount', models.FloatField()),
                ('code', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
