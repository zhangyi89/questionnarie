# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app01.Questionnaire'),
        ),
    ]
