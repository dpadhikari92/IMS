# Generated by Django 3.2.15 on 2023-07-08 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0009_auto_20230706_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitem',
            name='exp_date',
            field=models.DateField(blank=True, default='2023-07-08', null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='mfg_date',
            field=models.DateField(blank=True, default='2023-07-08', null=True),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='purchase_date',
            field=models.DateField(default='2023-07-08'),
        ),
        migrations.CreateModel(
            name='SfgBom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sfg', models.FloatField()),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.bom')),
                ('sfg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.production')),
            ],
        ),
    ]