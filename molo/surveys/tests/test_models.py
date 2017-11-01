from django.core.exceptions import ValidationError
from django.test import TestCase
from molo.core.tests.base import MoloTestCaseMixin
from molo.surveys.blocks import SkipLogicBlock, SkipState
from molo.surveys.models import (
    MoloSurveyFormField,
    MoloSurveyPage,
    MoloSurveySubmission,
)

from .utils import skip_logic_block_data, skip_logic_data


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
        self.normal_field = MoloSurveyFormField.objects.create(
            page=self.survey,
            sort_order=2,
            label='Your other favourite animal',
            field_type='singleline',
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

    def test_normal_field_is_not_skippable(self):
        self.assertFalse(self.normal_field.has_skipping)

    def test_only_next_doesnt_skip(self):
        self.assertFalse(self.choice_field.has_skipping)

    def test_other_logic_does_skip(self):
        self.choice_field.skip_logic = skip_logic_data(['choice'], ['end'])
        self.choice_field.save()
        self.assertTrue(self.choice_field.has_skipping)


class TestSkipLogicBlock(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.survey = MoloSurveyPage(
            title='Test Survey',
            slug='test-survey',
        )
        self.section_index.add_child(instance=self.survey)
        self.survey.save_revision().publish()

    def test_survey_raises_error_if_no_object(self):
        block = SkipLogicBlock()
        data = skip_logic_block_data(
            'next survey',
            SkipState.SURVEY,
            survey=None,
        )
        with self.assertRaises(ValidationError):
            block.clean(data)

    def test_survey_passes_with_object(self):
        block = SkipLogicBlock()
        data = skip_logic_block_data(
            'next survey',
            SkipState.SURVEY,
            survey=self.survey.id,
        )
        cleaned_data = block.clean(data)
        self.assertEqual(cleaned_data['skip_logic'], SkipState.SURVEY)
        self.assertEqual(cleaned_data['survey'], self.survey)

    def test_question_raises_error_if_no_object(self):
        block = SkipLogicBlock()
        data = skip_logic_block_data(
            'a question',
            SkipState.QUESTION,
            question=None,
        )
        with self.assertRaises(ValidationError):
            block.clean(data)

    def test_question_passes_with_object(self):
        block = SkipLogicBlock()
        data = skip_logic_block_data(
            'a question',
            SkipState.QUESTION,
            question=1,
        )
        cleaned_data = block.clean(data)
        self.assertEqual(cleaned_data['skip_logic'], SkipState.QUESTION)
        self.assertEqual(cleaned_data['question'], 1)
