# Generated by Django 5.0.6 on 2024-06-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_orders_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='customer',
            field=models.CharField(max_length=150),
        ),
    ]
