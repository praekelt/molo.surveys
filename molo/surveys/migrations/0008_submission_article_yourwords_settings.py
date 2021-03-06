# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-31 10:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_section_tags'),
        ('surveys', '0007_submit_text_percentage_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='molosurveypage',
            name='your_words_competition',
            field=models.BooleanField(default=False, help_text=b'This will display the correct template for yourwords', verbose_name=b'Is YourWords Competition'),
        ),
        migrations.AddField(
            model_name='molosurveysubmission',
            name='article_page',
            field=models.ForeignKey(blank=True, help_text=b'Page to which the entry was converted to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='core.ArticlePage'),
        ),
    ]
