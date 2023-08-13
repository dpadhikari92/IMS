# Generated by Django 3.2.15 on 2023-08-12 21:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0061_auto_20230810_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='exp',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='mfg',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='fgproduction',
            name='production_date',
            field=models.DateField(default='2023-08-12'),
        ),
        migrations.AlterField(
            model_name='production',
            name='production_date',
            field=models.DateField(default='2023-08-12'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(default='2023-08-12'),
        ),
    ]