# Generated by Django 3.2 on 2021-04-24 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0005_remove_barcode_inventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='code',
            field=models.CharField(blank=True, max_length=14, unique=True),
        ),
    ]
