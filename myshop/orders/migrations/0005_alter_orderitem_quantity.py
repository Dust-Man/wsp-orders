# Generated by Django 4.1.13 on 2025-03-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_tel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
        ),
    ]
