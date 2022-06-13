# Generated by Django 3.2.8 on 2021-11-09 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Inventory', '0008_auto_20211109_1715'),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.business')),
            ],
            options={
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sold', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Revenue.sales')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.CharField(max_length=64)),
                ('tax', models.CharField(blank=True, default=None, max_length=32, null=True)),
                ('total', models.CharField(default=None, max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventory.coupen')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Products.product')),
                ('saler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.business')),
            ],
        ),
    ]