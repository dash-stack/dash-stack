# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-20 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0018_remove_assignment_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='target',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='type',
            field=models.IntegerField(choices=[(1, 'UserProject'), (2, 'GroupProject'), (3, 'UserDomain'), (4, 'GroupDomain')], null=True),
        ),
    ]
