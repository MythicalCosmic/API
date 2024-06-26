# Generated by Django 5.0.6 on 2024-06-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_orders_price_alter_orders_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='services',
            field=models.ManyToManyField(related_name='doctors', to='main.service'),
        ),
        migrations.AddField(
            model_name='service',
            name='priceprice_of_service',
            field=models.IntegerField(null=True),
        ),
    ]
