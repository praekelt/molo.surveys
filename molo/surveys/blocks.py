from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField


class SkipLogicField(StreamField):
    def __init__(self, *args, **kwargs):
        args = [[('skip_logic', SkipLogicBlock())]]
        kwargs.update({
            'verbose_name': 'Answer options',
            'blank': True,
        })
        super(SkipLogicField, self).__init__(*args, **kwargs)


class SkipLogicStreamPanel(StreamFieldPanel):
    def bind_to_model(self, model):
        model_class = super(SkipLogicStreamPanel, self).bind_to_model(model)
        model_class.classname = 'skip-logic'
        return model_class


class SkipLogicBlock(blocks.StructBlock):
    choice = blocks.CharBlock()
    skip_logic = blocks.ChoiceBlock(
        choices=[
            ('next', 'Next default question'),
            ('end', 'End of survey'),
            ('another', 'Another survey'),
        ],
        default='next',
        required=True,
    )

    @property
    def media(self):
        return forms.Media(js=[static('js/blocks/skiplogic.js')])

    def js_initializer(self):
        opts = {}
        return "SkipLogic(%s)" % blocks.utils.js_dict(opts)
