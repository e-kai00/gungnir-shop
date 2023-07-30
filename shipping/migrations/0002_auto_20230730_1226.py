# Generated by Django 3.2.19 on 2023-07-30 10:26

import django.contrib.postgres.fields.ranges
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='delivery_time',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(default=(10, 21)),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='processing_time',
            field=models.IntegerField(default=1),
        ),
    ]