# Generated by Django 3.2.15 on 2023-08-13 23:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0069_auto_20230813_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasebilldetails',
            name='destination',
        ),
       
    ]
