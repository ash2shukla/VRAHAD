# Generated by Django 2.0.1 on 2018-01-07 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ASA', '0004_auto_20180107_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensekey',
            name='ts',
            field=models.CharField(default='1515365709', max_length=20),
        ),
    ]