# Generated by Django 5.1.1 on 2024-10-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='account_reference',
            field=models.CharField(default='default_reference', max_length=255),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_desc',
            field=models.CharField(default='default_description', max_length=255),
        ),
    ]
