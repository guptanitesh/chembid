# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-25 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_impurity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='pname',
        ),
        migrations.AddField(
            model_name='api',
            name='mainproduct',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='webapp.Mainproduct'),
        ),
        migrations.AddField(
            model_name='mainproduct',
            name='company_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='mainproduct',
            name='company_type',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='mainproduct',
            name='country',
            field=models.CharField(default='', max_length=200),
        ),
    ]
