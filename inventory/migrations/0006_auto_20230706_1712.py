# Generated by Django 3.2.15 on 2023-07-06 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_stock_cas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='cas',
            field=models.CharField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
