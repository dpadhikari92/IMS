# Generated by Django 3.2.15 on 2023-07-11 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_auto_20230711_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='fgproduction',
            name='production',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.production'),
        ),
    ]
