from django.db.models import Count
from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel, FieldPanel

from molo.core.models import ArticlePageTags


class BaseTagPanel(BaseFieldPanel):
    def __init__(self, *args, **kwargs):
        super(BaseTagPanel, self).__init__(*args, **kwargs)
        target_model = self.bound_field.field.queryset.model

        data = ArticlePageTags.objects.values('tag').annotate(
            count=Count('tag')
        )
        tag_count = {tag['tag']: tag['count'] for tag in data}

        self.bound_field.field.queryset = target_model.objects.filter(
            id__in=tag_count
        )

        self.bound_field.field.label_from_instance = (
            lambda obj: str(obj) + ' ({})'.format(tag_count[obj.id])
        )


class TagPanel(FieldPanel):
    def bind_to_model(self, model):
        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
        }

        if self.widget:
            base['widget'] = self.widget

        return type(str('_BaseTagPanel'), (BaseTagPanel,), base)
