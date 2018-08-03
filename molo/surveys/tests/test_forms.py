from __future__ import unicode_literals

from django.test import TestCase
from django.forms import ValidationError
from molo.surveys.forms import (
    CharacterCountWidget, MultiLineWidget, CharacterCountMixin)


class TestCharacterCountWidget(TestCase):
    def test_character_count_widget_render(self):
        widget = CharacterCountWidget()
        widget.attrs['maxlength'] = 10
        html = widget.render('field-name', 'field-value')
        self.assertTrue(html.endswith('<span>Maximum: 10</span>'))

    def test_character_count_widget_no_maxlength_raises_error(self):
        widget = CharacterCountWidget()
        with self.assertRaises(KeyError):
            widget.render('field-name', 'field-value')


class TestCharacterCountMixin(TestCase):
    def test_character_count_validation(self):
        class SMixin(object):
            error_messages = {}

            def validate(self, val):
                pass

        class TMixin(CharacterCountMixin, SMixin):
            pass
        # garbage validate func
        # garbage error message
        # prevent super error messages
        mixin = TMixin(max_length=2)
        with self.assertRaises(ValidationError):
            mixin.validate('maxlengthexceeded')


class TestMultiLineWidget(TestCase):
    def test_multi_line_widget_render(self):
        widget = MultiLineWidget()
        html = widget.render('field-name', 'field-value', {'my-attr': 1})
        self.assertTrue(html.endswith('<span>No limit</span>'))
