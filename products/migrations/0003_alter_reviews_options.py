# Generated by Django 3.2.19 on 2023-07-27 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_reviews'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ['-created_on'], 'verbose_name_plural': 'Reviews'},
        ),
    ]