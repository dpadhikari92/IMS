# Generated by Django 3.2.15 on 2023-08-12 22:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0062_auto_20230812_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
