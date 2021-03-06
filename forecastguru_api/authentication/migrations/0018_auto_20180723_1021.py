# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_auto_20180723_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='authentication',
            name='market_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='authentication',
            name='market_fee_paid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='authentication',
            name='successful_forecast',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='authentication',
            name='unsuccessful_forecast',
            field=models.IntegerField(default=0),
        ),
    ]
