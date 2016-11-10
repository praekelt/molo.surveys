# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 12:29
from __future__ import unicode_literals

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


class Migration(migrations.Migration):
    def add_surveys_permissions_to_groups(apps, schema_editor):
        db_alias = schema_editor.connection.alias
        try:
            # Django 1.9
            emit_post_migrate_signal(2, False, db_alias)
        except TypeError:
            # Django < 1.9
            try:
                # Django 1.8
                emit_post_migrate_signal(2, False, 'default', db_alias)
            except TypeError:  # Django < 1.8
                emit_post_migrate_signal([], 2, False, 'default', db_alias)

        Group = apps.get_model('auth.Group')
        GroupPagePermission = apps.get_model('wagtailcore.GroupPagePermission')
        SurveysIndexPage = apps.get_model('surveys.SurveysIndexPage')

        # Create groups

        # <- Editors ->
        editor_group = Group.objects.get(name='Editors')

        surveys = SurveysIndexPage.objects.first()
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=surveys,
            permission_type='add',
        )
        GroupPagePermission.objects.get_or_create(
            group=editor_group,
            page=surveys,
            permission_type='edit',
        )

        # <- Moderator ->
        moderator_group = Group.objects.get(name='Moderators')

        surveys = SurveysIndexPage.objects.first()
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=surveys,
            permission_type='add',
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=surveys,
            permission_type='edit',
        )
        GroupPagePermission.objects.get_or_create(
            group=moderator_group,
            page=surveys,
            permission_type='publish',
        )

    dependencies = [
        ('surveys', '0004_create_surveys_index_page'),
        ('core', '0047_add_core_permissions_to_groups'),
        ('contenttypes', '__latest__'),
        ('sites', '__latest__'),
    ]

    operations = [
        migrations.RunPython(add_surveys_permissions_to_groups),
    ]
