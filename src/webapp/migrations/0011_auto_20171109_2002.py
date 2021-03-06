# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-09 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20171026_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='company_type',
            field=models.CharField(choices=[('Manufacturer', 'Manufacturer'), ('Trader', 'Trader')], default='', max_length=12),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_no',
            field=models.IntegerField(default=0),
        ),
    ]
