# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-09 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20171109_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='components',
        ),
        migrations.AddField(
            model_name='product',
            name='Cas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='grade',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
