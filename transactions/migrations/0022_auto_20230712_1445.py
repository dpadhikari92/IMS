# Generated by Django 3.2.15 on 2023-07-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0021_auto_20230712_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseitem',
            name='exp_date',
        ),
        migrations.RemoveField(
            model_name='purchaseitem',
            name='mfg_date',
        ),
        migrations.AddField(
            model_name='purchasebilldetails',
            name='exp_date',
            field=models.DateField(default='2023-07-12'),
        ),
        migrations.AddField(
            model_name='purchasebilldetails',
            name='mfg_date',
            field=models.DateField(default='2023-07-12'),
        ),
    ]
