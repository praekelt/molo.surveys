from __future__ import unicode_literals

from django.test import TestCase

from molo.surveys.forms import CharacterCountWidget, MultiLineWidget


class TestCharacterCountWidget(TestCase):
    def test_character_count_widget_render(self):
        widget = CharacterCountWidget()
        html = widget.render('field-name', 'field-value', {'maxlength': 10})
        self.assertEqual(
            html,
            ('<input  maxlength="10" name="field-name" '
             'type="text" value="field-value" /><span>Maximum: 10</span>')
        )

    def test_character_count_widget_no_maxlength_raises_error(self):
        widget = CharacterCountWidget()
        with self.assertRaises(KeyError):
            widget.render('field-name', 'field-value')


class TestMultiLineWidget(TestCase):
    def test_multi_line_widget_render(self):
        widget = MultiLineWidget()
        html = widget.render('field-name', 'field-value', {'my-attr': 1})
        self.assertEqual(
            html,
            ('<textarea cols="40" my-attr="1" name="field-name" rows="10">'
             '\r\nfield-value</textarea><span>No limit</span>')
        )
