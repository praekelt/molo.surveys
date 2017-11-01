from collections import defaultdict
import datetime

from wagtail_personalisation.adapters import SessionSegmentsAdapter
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from molo.core.models import ArticlePage


class SurveysSegmentsAdapter(SessionSegmentsAdapter):
    def add_page_visit(self, page):
        super(SurveysSegmentsAdapter, self).add_page_visit(page)
        tag_visits = self.request.session.setdefault(
            'tag_count',
            defaultdict(dict),
        )
        if isinstance(page.specific, ArticlePage):
            # Set the datetime based on UTC
            visit_time = datetime.datetime.now(timezone.utc).isoformat()
            for nav_tag in page.nav_tags.all():
                tag_visits.setdefault(str(nav_tag.tag.id), dict())
                tag_visits[str(nav_tag.tag.id)][page.path] = visit_time

    def get_tag_count(self, tag, date_from=None, date_to=None):
        """Return the number of visits on the given page"""
        if not date_from:
            date_from = timezone.make_aware(
                datetime.datetime.min,
                timezone.utc,
            )
        if not date_to:
            date_to = timezone.make_aware(
                datetime.datetime.max,
                timezone.utc,
            )

        tag_visits = self.request.session.setdefault(
            'tag_count',
            defaultdict(dict),
        )

        visits = tag_visits.get(str(tag.id), dict())
        valid_visits = [visit for visit in visits.values()
                        if date_from <= parse_datetime(visit) <= date_to]
        return len(valid_visits)
