# Generated by Django 3.2.15 on 2023-07-08 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0011_sfgproduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sfgbom',
            name='bom',
        ),
        migrations.CreateModel(
            name='Sfgfinal',
            fields=[
                ('id', models.AutoField(default=1,auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.bom')),
                ('sfg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.sfgbom')),
            ],
        ),
    ]
