# Generated by Django 3.2.15 on 2023-08-07 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0037_remove_purchasebilldetails_purchaseitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebill',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
