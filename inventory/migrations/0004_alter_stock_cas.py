# Generated by Django 3.2.15 on 2023-06-21 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20230617_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='cas',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
