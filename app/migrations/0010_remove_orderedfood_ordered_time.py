# Generated by Django 5.2.1 on 2025-06-07 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_ordering_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderedfood',
            name='ordered_time',
        ),
    ]
