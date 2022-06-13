# Generated by Django 3.2.8 on 2021-11-09 11:45

import Barcode.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Barcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=14, unique=True)),
                ('barcodeimage', models.ImageField(blank=True, upload_to=Barcode.models.product_code_directory_path)),
                ('qrcodeimage', models.ImageField(blank=True, upload_to=Barcode.models.product_code_directory_path)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Products.product')),
            ],
        ),
    ]
