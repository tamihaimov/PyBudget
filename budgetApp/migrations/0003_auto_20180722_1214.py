# Generated by Django 2.0.6 on 2018-07-22 09:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0002_budgetaccount_last_reset_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetaccount',
            name='last_reset_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 22, 12, 14, 1, 953563)),
        ),
    ]