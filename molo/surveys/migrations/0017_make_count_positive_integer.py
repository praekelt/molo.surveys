# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-24 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_articletagrule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletagrule',
            name='count',
            field=models.PositiveIntegerField(),
        ),
    ]
