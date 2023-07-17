# Generated by Django 3.2.15 on 2023-07-08 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0010_auto_20230708_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='sfgproduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('production_date', models.DateField(auto_now_add=True)),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.sfgbom')),
            ],
        ),
    ]
