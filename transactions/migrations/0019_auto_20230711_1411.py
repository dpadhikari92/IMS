# Generated by Django 3.2.15 on 2023-07-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_fgproduction_production'),
    ]

    operations = [
        migrations.AddField(
            model_name='fgproduction',
            name='code_fg',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fgsfg',
            name='code',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]