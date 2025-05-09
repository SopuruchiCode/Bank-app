# Generated by Django 4.2 on 2024-09-30 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_API', '0010_delete_paymentlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('processing_fee', models.DecimalField(decimal_places=2, max_digits=15)),
                ('merchant_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment_API.epaymentsubscription')),
                ('client_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='openaccount.account')),
            ],
        ),
    ]
