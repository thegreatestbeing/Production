# Generated by Django 3.2.8 on 2021-11-09 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Search', '0002_alter_keywords_keyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keywords',
            options={'verbose_name': 'Keyword', 'verbose_name_plural': 'keywords'},
        ),
    ]
