# Generated by Django 3.2.15 on 2023-07-14 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0026_auto_20230714_0632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fgsfgnew',
            old_name='raw_materials',
            new_name='raw_material',
        ),
    ]
