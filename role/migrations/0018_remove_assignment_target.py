# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-20 17:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0017_auto_20170420_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='target',
        ),
    ]
