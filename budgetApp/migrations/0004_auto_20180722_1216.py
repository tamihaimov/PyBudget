# Generated by Django 2.0.6 on 2018-07-22 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0003_auto_20180722_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgetaccount',
            name='last_reset_date',
            field=models.DateField(default=datetime.datetime(2018, 7, 22, 9, 16, 40, 486652, tzinfo=utc)),
        ),
    ]
