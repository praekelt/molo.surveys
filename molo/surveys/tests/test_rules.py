import datetime
import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from django.utils import timezone
from wagtail_personalisation.adapters import get_segment_adapter

from molo.core.models import ArticlePage, ArticlePageTags, SectionPage, Tag
from molo.core.tests.base import MoloTestCaseMixin
from molo.surveys.models import SurveysIndexPage


from .utils import skip_logic_data
from ..models import (
    PersonalisableSurveyFormField,
    PersonalisableSurvey,
    SegmentUserGroup,
)
from ..rules import (
    ArticleTagRule,
    GroupMembershipRule,
    SurveySubmissionDataRule,
)


@pytest.mark.django_db
class TestSurveyDataRuleSegmentation(TestCase, MoloTestCaseMixin):
    def setUp(self):
        # Fabricate a request with a logged-in user
        # so we can use it to test the segment rule
        self.mk_main()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        self.request.user = get_user_model().objects.create_user(
            username='tester', email='tester@example.com', password='tester')

        # Create survey
        self.survey = PersonalisableSurvey(title='Test Survey')
        SurveysIndexPage.objects.first().add_child(instance=self.survey)

        # Create survey form fields
        self.singleline_text = PersonalisableSurveyFormField.objects.create(
            field_type='singleline', label='Singleline Text', page=self.survey)
        self.checkboxes = PersonalisableSurveyFormField.objects.create(
            field_type='checkboxes', label='Checboxes Field', page=self.survey,
            skip_logic=skip_logic_data(['choice 1', 'choice 2', 'choice 3']))
        self.checkbox = PersonalisableSurveyFormField.objects.create(
            field_type='checkbox', label='Checbox Field', page=self.survey)
        self.number = PersonalisableSurveyFormField.objects.create(
            field_type='number', label='Number Field', page=self.survey)

        # Create survey submission
        data = {
            self.singleline_text.clean_name: 'super random text',
            self.checkboxes.clean_name: ['choice 3', 'choice 1'],
            self.checkbox.clean_name: True,
            self.number.clean_name: 5
        }
        form = self.survey.get_form(
            data, page=self.survey, user=self.request.user)

        assert form.is_valid(), \
            'Could not validate submission form. %s' % repr(form.errors)

        self.survey.process_form_submission(form)

        self.survey.refresh_from_db()

    def test_passing_string_rule_with_equal_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.EQUALS,
            expected_response='super random text',
            field_name=self.singleline_text.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_string_rule_with_equal_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.EQUALS,
            expected_response='super random textt',
            field_name=self.singleline_text.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_passing_string_rule_with_contain_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='text',
            field_name=self.singleline_text.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_string_rule_with_contain_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='word',
            field_name=self.singleline_text.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_padding_checkboxes_rule_with_equal_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response=' choice 3 , choice 1 ',
            field_name=self.checkboxes.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_checkboxes_rule_with_equal_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='choice2,choice1',
            field_name=self.checkboxes.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_passing_checkboxes_rule_with_contain_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='choice 3',
            field_name=self.checkboxes.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_checkboxes_rule_with_contain_operator(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='choice 2, choice 3',
            field_name=self.checkboxes.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_passing_checkbox_rule(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='1',
            field_name=self.checkbox.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_checkbox_rule(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='0',
            field_name=self.checkbox.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_passing_number_rule(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='5',
            field_name=self.number.clean_name)

        self.assertTrue(rule.test_user(self.request))

    def test_failing_number_rule(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='4',
            field_name=self.number.clean_name)

        self.assertFalse(rule.test_user(self.request))

    def test_not_logged_in_user_fails(self):
        rule = SurveySubmissionDataRule(
            survey=self.survey, operator=SurveySubmissionDataRule.CONTAINS,
            expected_response='er ra',
            field_name=self.singleline_text.clean_name)

        # Passes for logged-in user
        self.assertTrue(rule.test_user(self.request))

        # Fails for logged-out user
        self.request.user = AnonymousUser()
        self.assertFalse(rule.test_user(self.request))


class TestGroupMembershipRuleSegmentation(TestCase, MoloTestCaseMixin):
    def setUp(self):
        # Fabricate a request with a logged-in user
        # so we can use it to test the segment rule
        self.mk_main()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        self.request.user = get_user_model().objects.create_user(
            username='tester', email='tester@example.com', password='tester')

        self.group = SegmentUserGroup.objects.create(name='Super Test Group!')

        self.request.user.segment_groups.add(self.group)

    def test_user_membership_rule_when_they_are_member(self):
        rule = GroupMembershipRule(group=self.group)

        self.assertTrue(rule.test_user(self.request))

    def test_user_membership_rule_when_they_are_not_member(self):
        group = SegmentUserGroup.objects.create(name='Wagtail-like creatures')
        rule = GroupMembershipRule(group=group)

        self.assertFalse(rule.test_user(self.request))

    def test_user_membership_rule_on_not_logged_in_user(self):
        self.request.user = AnonymousUser()
        rule = GroupMembershipRule(group=self.group)

        self.assertFalse(rule.test_user(self.request))


class TestArticleTagRuleSegmentation(TestCase, MoloTestCaseMixin):
    def setUp(self):
        # Fabricate a request with a logged-in user
        # so we can use it to test the segment rule
        self.mk_main()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

        self.section = SectionPage(title='test section')
        self.section_index.add_child(instance=self.section)

        self.tag = Tag(title='test')
        self.tag_index.add_child(instance=self.tag)
        self.tag.save_revision()

        self.article = self.add_article(title='test article', tags=[self.tag])

        self.adapter = get_segment_adapter(self.request)

    def add_article(self, title, tags):
        new_article = ArticlePage(title=title)
        self.section.add_child(instance=new_article)
        new_article.save_revision()
        for tag in tags:
            ArticlePageTags.objects.create(
                tag=tag,
                page=new_article,
            )
        return new_article

    def test_user_visits_page_with_tag(self):
        rule = ArticleTagRule(
            operator=ArticleTagRule.EQUALS,
            tag=self.tag,
            count=1,
        )

        self.adapter.add_page_visit(self.article)

        self.assertTrue(rule.test_user(self.request))

    def test_user_tag_with_no_visits(self):
        rule = ArticleTagRule(tag=self.tag, count=1)

        self.assertFalse(rule.test_user(self.request))

    def test_user_visits_page_twice_tag_not_duplicated(self):
        rule = ArticleTagRule(
            operator=ArticleTagRule.EQUALS,
            tag=self.tag,
            count=1,
        )

        self.adapter.add_page_visit(self.article)
        self.adapter.add_page_visit(self.article)

        self.assertTrue(rule.test_user(self.request))

    def test_user_visits_page_after_cutoff(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=1,
            date_to=timezone.make_aware(
                datetime.datetime.now() - datetime.timedelta(days=1)
            ),
        )

        self.adapter.add_page_visit(self.article)
        self.adapter.add_page_visit(self.article)

        self.assertFalse(rule.test_user(self.request))

    def test_user_visits_two_different_pages_same_tag(self):
        rule = ArticleTagRule(
            operator=ArticleTagRule.EQUALS,
            tag=self.tag,
            count=2,
        )
        new_article = self.add_article(title='new article', tags=[self.tag])

        self.adapter.add_page_visit(self.article)
        self.adapter.add_page_visit(new_article)

        self.assertTrue(rule.test_user(self.request))

    def test_user_passes_less_than(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=2,
            operator=ArticleTagRule.LESS_THAN,
        )
        self.adapter.add_page_visit(self.article)
        self.assertTrue(rule.test_user(self.request))

    def test_user_fails_less_than(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=1,
            operator=ArticleTagRule.LESS_THAN,
        )
        self.adapter.add_page_visit(self.article)
        self.assertFalse(rule.test_user(self.request))

    def test_user_fails_greater_than(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=1,
            operator=ArticleTagRule.GREATER_THAN,
        )
        self.adapter.add_page_visit(self.article)
        self.assertFalse(rule.test_user(self.request))

    def test_user_passes_greater_than(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=0,
            operator=ArticleTagRule.GREATER_THAN,
        )
        self.adapter.add_page_visit(self.article)
        self.assertTrue(rule.test_user(self.request))

    def test_dates_are_in_order(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=1,
            date_from=datetime.datetime.now(),
            date_to=datetime.datetime.now() - datetime.timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            rule.clean()

    def test_count_more_than_article_error(self):
        rule = ArticleTagRule(
            tag=self.tag,
            count=2,
        )
        with self.assertRaises(ValidationError):
            rule.clean()

    def test_visting_non_tagged_page_isnt_error(self):
        self.adapter.add_page_visit(self.main)
        self.assertFalse(self.request.session['tag_count'])
