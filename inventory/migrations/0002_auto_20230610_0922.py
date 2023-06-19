# Generated by Django 3.0.7 on 2023-06-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='cas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='hsn',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stock',
            name='item_code',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='quantity',
            field=models.FloatField(default=0),
        ),
    ]
