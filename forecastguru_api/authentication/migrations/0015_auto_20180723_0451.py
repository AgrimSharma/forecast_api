# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-23 04:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_auto_20180719_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest', models.ManyToManyField(to='authentication.SubCategory')),
            ],
            options={
                'ordering': ['-user'],
                'verbose_name_plural': 'User Interest',
            },
        ),
        migrations.AlterModelOptions(
            name='authentication',
            options={'ordering': ['-email']},
        ),
        migrations.AlterModelOptions(
            name='dailyfreepoints',
            options={'ordering': ['days'], 'verbose_name_plural': 'Daily Bonus'},
        ),
        migrations.AlterField(
            model_name='authentication',
            name='last_login',
            field=models.DateField(default=datetime.date(2018, 7, 23)),
        ),
        migrations.AddField(
            model_name='userinterest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Authentication'),
        ),
    ]
