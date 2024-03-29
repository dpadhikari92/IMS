# Generated by Django 3.2.15 on 2023-07-12 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0023_purchasebilldetails_sup_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='exp_date',
        ),
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='mfg_date',
        ),
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='sup_invoice',
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='exp_date',
            field=models.DateField(blank=True, default='2023-07-12', null=True),
        ),
        migrations.AddField(
            model_name='purchaseitem',
            name='mfg_date',
            field=models.DateField(blank=True, default='2023-07-12', null=True),
        ),
    ]
