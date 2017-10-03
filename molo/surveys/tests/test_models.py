from django.test import TestCase
from molo.core.tests.base import MoloTestCaseMixin
from molo.surveys.models import MoloSurveyPage, MoloSurveySubmission, MoloSurveyFormField

from .utils import skip_logic_data

class TestSurveyModels(TestCase, MoloTestCaseMixin):
    def test_submission_class(self):
        submission_class = MoloSurveyPage().get_submission_class()

        self.assertIs(submission_class, MoloSurveySubmission)

    def test_submission_class_get_data_includes_username(self):
        data = MoloSurveyPage().get_submission_class()(
            form_data='{}'
        ).get_data()
        self.assertIn('username', data)


class TestSkipLogicMixin(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.field_choices = ['old', 'this', 'is']
        self.survey = MoloSurveyPage(
            title='Test Survey',
            slug='test-survey',
        )
        self.section_index.add_child(instance=self.survey)
        self.survey.save_revision().publish()
        self.choice_field = MoloSurveyFormField.objects.create(
            page=self.survey,
            sort_order=1,
            label='Your favourite animal',
            field_type='dropdown',
            skip_logic=skip_logic_data(self.field_choices),
            required=True
        )

    def test_choices_updated_from_streamfield_on_save(self):
        self.assertEqual(
            ','.join(self.field_choices),
            self.choice_field.choices
        )

        new_choices = ['this', 'is', 'new']
        self.choice_field.skip_logic = skip_logic_data(new_choices)
        self.choice_field.save()

        self.assertEqual(','.join(new_choices), self.choice_field.choices)
