# Generated by Django 3.2.15 on 2023-08-08 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20230706_1712'),
        ('transactions', '0046_purchasebilldetails_purchase_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='purchase_code',
        ),
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='stocks',
        ),
        migrations.CreateModel(
            name='PurchaseCodeCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('stock', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_code_counter', to='inventory.stock')),
            ],
        ),
    ]
