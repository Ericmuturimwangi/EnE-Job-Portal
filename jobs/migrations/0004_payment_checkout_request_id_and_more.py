# Generated by Django 5.1.1 on 2024-10-01 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_payment_account_reference_payment_transaction_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='checkout_request_id',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='merchant_request_id',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
