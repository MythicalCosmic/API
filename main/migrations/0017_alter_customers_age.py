# Generated by Django 5.0.6 on 2024-07-01 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_doctors_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
