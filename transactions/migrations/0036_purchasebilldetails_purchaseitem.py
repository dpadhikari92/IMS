# Generated by Django 3.2.15 on 2023-08-07 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0035_purchasebilldetails_receipt_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasebilldetails',
            name='purchaseItem',
            field=models.ForeignKey(default=61, on_delete=django.db.models.deletion.CASCADE, to='transactions.purchaseitem'),
            preserve_default=False,
        ),
    ]