# Generated by Django 5.0 on 2024-01-15 19:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0005_alter_order_is_due_date_adjustable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_due_date_adjustable',
        ),
        migrations.AlterField(
            model_name='order',
            name='data_intrare',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data Intrare'),
        ),
    ]
