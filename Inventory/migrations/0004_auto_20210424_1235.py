# Generated by Django 3.2 on 2021-04-24 07:05

import Inventory.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0003_auto_20210423_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='barcode',
        ),
        migrations.RemoveField(
            model_name='product',
            name='code',
        ),
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=12, unique=True)),
                ('barcodeimage', models.ImageField(blank=True, upload_to=Inventory.models.product_code_directory_path)),
                ('qrcodeimage', models.ImageField(blank=True, upload_to=Inventory.models.product_code_directory_path)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.inventory')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Inventory.product')),
            ],
        ),
    ]