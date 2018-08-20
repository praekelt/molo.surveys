# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-20 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0027_override-512-char-limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='molosurveyformfield',
            name='choices',
            field=models.TextField(blank=True, help_text='Comma separated list of choices. Only applicable in checkboxes,radio and dropdown. The full length of the choice list and the commas that separate them are resctricted to 512 characters.', verbose_name='choices'),
        ),
    ]
