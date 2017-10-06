from __future__ import unicode_literals

from django.core.paginator import Paginator, Page
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.functional import cached_property

from .blocks import SkipState


class SkipLogicPaginator(Paginator):
    def __init__(self, object_list, data=dict()):
        self.data = data
        super(SkipLogicPaginator, self).__init__(object_list, per_page=1)
        self.skip_indexes = [
            i + 1 for i, field in enumerate(self.object_list) if field.has_skipping
        ]
        if self.skip_indexes:
            self.skip_indexes = [0] + self.skip_indexes + [self.object_list.count()]
        else:
            self.skip_indexes = range(self.object_list.count() + 1)

    def _get_page(self, *args, **kwargs):
        return SkipLogicPage(*args, **kwargs)

    @cached_property
    def num_pages(self):
        return len(self.skip_indexes) - 1

    def page(self, number):
        number = self.validate_number(number)
        bottom_index = (number - 1)
        top_index = bottom_index + self.per_page
        bottom = self.skip_indexes[bottom_index]
        top = self.skip_indexes[top_index]
        return self._get_page(self.object_list[bottom:top], number, self)


class SkipLogicPage(Page):
    def has_next(self):
        return super(SkipLogicPage, self).has_next() and not self.is_end()

    @cached_property
    def last_question(self):
        return self.object_list[-1]

    @cached_property
    def last_response(self):
        return self.paginator.data[self.last_question.clean_name]

    def is_next_action(self, *actions):
        try:
            question_response = self.last_response
        except KeyError:
            return False
        if self.last_question.has_skipping:
            return self.last_question.next_action(question_response) in actions
        return False

    def is_end(self):
        return self.is_next_action(SkipState.END, SkipState.SURVEY)

    def success(self, slug):
        if self.is_next_action(SkipState.SURVEY):
            return redirect(
                self.last_question.next_page(self.last_response).url
            )
        return redirect(
            reverse('molo.surveys:success', args=(slug, ))
        )