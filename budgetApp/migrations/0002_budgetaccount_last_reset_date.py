# Generated by Django 2.0.6 on 2018-07-22 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetaccount',
            name='last_reset_date',
            field=models.DateField(default=datetime.date(2018, 7, 22)),
        ),
    ]
