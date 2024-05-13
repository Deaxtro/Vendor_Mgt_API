# Generated by Django 5.0.4 on 2024-05-11 17:13

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='po',
            name='acknowledgment_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='po',
            name='po_number',
            field=models.CharField(default=builtins.id, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='po',
            name='quality_rating',
            field=models.FloatField(null=True),
        ),
    ]
