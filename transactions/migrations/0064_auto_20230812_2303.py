# Generated by Django 3.2.15 on 2023-08-12 23:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0063_alter_purchaseitem_purchase_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='coa',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='exp',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='mfg',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]