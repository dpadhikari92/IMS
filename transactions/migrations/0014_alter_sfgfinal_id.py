# Generated by Django 3.2.15 on 2023-07-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_auto_20230710_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sfgfinal',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
