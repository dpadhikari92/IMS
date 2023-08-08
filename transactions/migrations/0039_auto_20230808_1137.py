# Generated by Django 3.2.15 on 2023-08-08 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0038_alter_purchasebill_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='exp_date',
            field=models.DateField(blank=True, default='2023-08-08', null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='mfg_date',
            field=models.DateField(blank=True, default='2023-08-08', null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(default='2023-08-08'),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='supplier_no',
            field=models.CharField(blank=True, default=1, max_length=12, null=True),
        ),
    ]