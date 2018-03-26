from django.core.exceptions import ValidationError
from django.test import TestCase
from molo.core.tests.base import MoloTestCaseMixin
from django.test.client import Client
from molo.core.models import Languages, Main
from molo.surveys.blocks import SkipLogicBlock, SkipState
from molo.surveys.models import (
    MoloSurveyFormField,
    MoloSurveyPage,
    MoloSurveySubmission,
    SurveysIndexPage,
    PersonalisableSurvey,
    PersonalisableSurveyFormField
)

from .utils import skip_logic_block_data, skip_logic_data
from .base import create_survey


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
        self.positive_number_field = MoloSurveyFormField.objects.create(
            page=self.survey,
            sort_order=3,
            label='How old are you',
            field_type='positive_number',
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

    def test_positive_number_field_is_not_skippable(self):
        self.assertFalse(self.positive_number_field.has_skipping)

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


class TestPageBreakWithTwoQuestionsInOneStep(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.login()

    def test_setup(self):
        self.assertEquals(1, SurveysIndexPage.objects.count())

        create_survey()

        self.assertEquals(1, MoloSurveyPage.objects.count())

    def test_setup2(self):
        create_survey([{
            "question":
                "Why do you feel that way about speaking your opinion?",
            "type": 'multiline',
            "required": False,
            "page_break": True,
        }, ])

        self.assertEquals(1, MoloSurveyPage.objects.count())

    def test_two_questions_in_one_step_when_one_required(self):
        create_survey([
            {
                "question": "I feel I can be myself around other people",
                "type": 'radio',
                "choices": ["agree", "disagree"],
                "required": True,
                "page_break": True,
            },
            {
                "question": "I can speak my opinion",
                "type": 'radio',
                "choices": ["yes", "no", "maybe"],
                "required": True,
                "page_break": False,
            },
            {
                "question":
                    "Why do you feel that way about speaking your opinion?",
                "type": 'multiline',
                "required": False,
                "page_break": True,
            },
            {
                "question":
                    "I am able to stand up for myself and what I believe in",
                "type": 'radio',
                "choices": ["Strongly disagree", "I don't know"],
                "required": True,
                "page_break": False,
            },
        ])

        self.assertEquals(1, MoloSurveyPage.objects.count())

        survey = MoloSurveyPage.objects.last()

        self.assertEquals(4, survey.survey_form_fields.count())

        field_1 = survey.survey_form_fields.all()[0]

        self.assertEquals(
            field_1.skip_logic.stream_data[0]['value']['choice'],
            "agree"
        )
        self.assertEquals(
            field_1.skip_logic.stream_data[0]['value']['skip_logic'],
            "next"
        )
        self.assertEquals(field_1.sort_order, 0)

        field_2 = survey.survey_form_fields.all()[1]

        self.assertEquals(
            field_2.skip_logic.stream_data[0]['value']['choice'],
            "yes"
        )
        self.assertEquals(
            field_2.skip_logic.stream_data[0]['value']['skip_logic'],
            "next"
        )
        self.assertEquals(field_2.sort_order, 1)

        field_3 = survey.survey_form_fields.all()[2]
        self.assertEquals(field_3.sort_order, 2)

        field_4 = survey.survey_form_fields.all()[3]

        self.assertEquals(
            field_4.skip_logic.stream_data[0]['value']['choice'],
            "Strongly disagree"
        )
        self.assertEquals(
            field_4.skip_logic.stream_data[0]['value']['skip_logic'],
            "next"
        )
        self.assertEquals(field_4.sort_order, 3)

        response = self.client.get(survey.url)

        self.assertContains(response, field_1.label)
        self.assertContains(response, 'Next Question')
        self.assertContains(response, 'action="' + survey.url + '?p=2"')

        response = self.client.post(survey.url + '?p=2', {
            field_1.clean_name:
                field_1.skip_logic.stream_data[0]['value']['choice'],
        })
        self.assertContains(response, field_2.label)
        self.assertContains(response, field_3.label)

        response = self.client.post(survey.url + '?p=3', {
            field_3.clean_name: 'because ;)',
        }, follow=True)

        self.assertContains(response, "This field is required")
        self.assertContains(response, 'action="' + survey.url + '?p=3"')

        response = self.client.post(survey.url + '?p=3', {
            field_2.clean_name:
                field_2.skip_logic.stream_data[0]['value']['choice'],
            field_3.clean_name: 'because ;)',
        })

        self.assertContains(response, field_4.label)

        response = self.client.post(survey.url + '?p=4', follow=True)
        self.assertContains(response, "This field is required")

        response = self.client.post(survey.url + '?p=4', {
            field_4.clean_name:
                field_4.skip_logic.stream_data[0]['value']['choice'],
        }, follow=True)

        self.assertContains(response, survey.thank_you_text)

    def test_two_questions_in_last_step_when_one_required(self):
        create_survey([
            {
                "question": "I feel I can be myself around other people",
                "type": 'radio',
                "choices": ["agree", "disagree"],
                "required": True,
                "page_break": True,
            },
            {
                "question": "I can speak my opinion",
                "type": 'radio',
                "choices": ["yes", "no", "maybe"],
                "required": True,
                "page_break": False,
            },
            {
                "question":
                    "Why do you feel that way about speaking your opinion?",
                "type": 'multiline',
                "required": False,
                "page_break": False,
            },
        ])

        self.assertEquals(1, MoloSurveyPage.objects.count())

        survey = MoloSurveyPage.objects.last()

        self.assertEquals(3, survey.survey_form_fields.count())

        field_1 = survey.survey_form_fields.all()[0]

        self.assertEquals(
            field_1.skip_logic.stream_data[0]['value']['choice'],
            "agree"
        )
        self.assertEquals(
            field_1.skip_logic.stream_data[0]['value']['skip_logic'],
            "next"
        )
        self.assertEquals(field_1.sort_order, 0)

        field_2 = survey.survey_form_fields.all()[1]

        self.assertEquals(
            field_2.skip_logic.stream_data[0]['value']['choice'],
            "yes"
        )
        self.assertEquals(
            field_2.skip_logic.stream_data[0]['value']['skip_logic'],
            "next"
        )
        self.assertEquals(field_2.sort_order, 1)

        field_3 = survey.survey_form_fields.all()[2]
        self.assertEquals(field_3.sort_order, 2)

        response = self.client.get(survey.url)

        self.assertContains(response, field_1.label)
        self.assertContains(response, 'Next Question')

        response = self.client.post(survey.url + '?p=2', {
            field_1.clean_name:
                field_1.skip_logic.stream_data[0]['value']['choice'],
        })
        self.assertContains(response, field_2.label)
        self.assertContains(response, field_3.label)

        response = self.client.post(survey.url + '?p=3', {
            field_3.clean_name: 'because ;)',
        }, follow=True)

        self.assertContains(response, "This field is required")
        response = self.client.post(survey.url + '?p=3', {
            field_2.clean_name:
                field_2.skip_logic.stream_data[0]['value']['choice'],
            field_3.clean_name: 'because ;)',
        }, follow=True)
        self.assertContains(response, survey.thank_you_text)


class TestFormFieldDefaultDateValidation(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()

    def create_molo_survey_form_field(self, field_type):
        survey = MoloSurveyPage(
            title='Test Survey',
            introduction='Introduction to Test Survey ...',
        )
        SurveysIndexPage.objects.first().add_child(instance=survey)
        survey.save_revision().publish()

        return MoloSurveyFormField.objects.create(
            page=survey,
            label="When is your birthday",
            field_type=field_type,
            admin_label="birthday",
        )

    def create_personalisable_survey_form_field(self, field_type):
        survey = PersonalisableSurvey(
            title='Test Survey',
            introduction='Introduction to Test Survey ...',
        )

        SurveysIndexPage.objects.first().add_child(instance=survey)
        survey.save_revision().publish()

        return PersonalisableSurveyFormField.objects.create(
            page=survey,
            label="When is your birthday",
            field_type=field_type,
            admin_label="birthday",
        )

    def test_date_molo_form_fields_clean_if_blank(self):
        field = self.create_molo_survey_form_field('date')
        field.default_value = ""
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_date_molo_form_fields_clean_with_valid_default(self):
        field = self.create_molo_survey_form_field('date')
        field.default_value = "2008-05-05"
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_date_molo_form_fields_not_clean_with_invalid_default(self):
        field = self.create_molo_survey_form_field('date')
        field.default_value = "something that isn't a date"
        with self.assertRaises(ValidationError) as e:
            field.clean()

        self.assertEqual(e.exception.messages, ['Must be a valid date'])

    def test_datetime_molo_form_fields_clean_if_blank(self):
        field = self.create_molo_survey_form_field('datetime')
        field.default_value = ""
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_datetime_molo_form_fields_clean_with_valid_default(self):
        field = self.create_molo_survey_form_field('datetime')
        field.default_value = "2008-05-05"
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_datetime_molo_form_fields_not_clean_with_invalid_default(self):
        field = self.create_molo_survey_form_field('datetime')
        field.default_value = "something that isn't a date"
        with self.assertRaises(ValidationError) as e:
            field.clean()

        self.assertEqual(e.exception.messages, ['Must be a valid date'])

    def test_date_personalisabe_form_fields_clean_if_blank(self):
        field = self.create_personalisable_survey_form_field('date')
        field.default_value = ""
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_date_personalisabe_form_fields_clean_with_valid_default(self):
        field = self.create_personalisable_survey_form_field('date')
        field.default_value = "2008-05-05"
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_date_personalisable_fields_not_clean_with_invalid_default(self):
        field = self.create_personalisable_survey_form_field('date')
        field.default_value = "something that isn't a date"
        with self.assertRaises(ValidationError) as e:
            field.clean()

        self.assertEqual(e.exception.messages, ['Must be a valid date'])

    def test_datetime_personalisabe_form_fields_clean_if_blank(self):
        field = self.create_personalisable_survey_form_field('datetime')
        field.default_value = ""
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_datetime_personalisabe_form_fields_clean_with_valid_default(self):
        field = self.create_personalisable_survey_form_field('datetime')
        field.default_value = "2008-05-05"
        try:
            field.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError with valid content!")

    def test_datetime_personalisable_fields_not_clean_with_invalid_default(
            self):
        field = self.create_personalisable_survey_form_field('datetime')
        field.default_value = "something that isn't a date"
        with self.assertRaises(ValidationError) as e:
            field.clean()

        self.assertEqual(e.exception.messages, ['Must be a valid date'])


class TestPollsViaSurveys(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.login()
        self.client = Client()
        self.main = Main.objects.all().first()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)

    def test_molo_survey_poll(self):
        survey = MoloSurveyPage(
            title='Molo Survey Poll ',
            slug="molo-survey-poll",
            introduction='Introduction to Test Survey ...',
            allow_anonymous_submissions=True,
            display_survey_directly=True,
            allow_multiple_submissions_per_user=True,
            thank_you_text='Thank you for taking the Molo Poll',
        )

        SurveysIndexPage.objects.first().add_child(instance=survey)
        survey.save_revision().publish()
        choices = ['next', 'end', 'survey']

        drop_down_field = MoloSurveyFormField.objects.create(
            page=survey,
            sort_order=1,
            admin_label="where",
            label='Where should we go?',
            field_type='dropdown',
            skip_logic=skip_logic_data(choices),
            required=True,
            page_break=True
        )
        response = self.client.post(
            survey.url + '?p=1',
            {drop_down_field.clean_name: 'next'},
            follow=True,
        )
        self.assertContains(response, survey.thank_you_text)
        self.assertNotContains(response, 'That page number is less than 1')

    def test_personalisable_survey_poll(self):
        survey = PersonalisableSurvey(
            title='Personalisable Survey Poll',
            slug="personalisable-survey-poll",
            introduction='Introduction to Test Survey ...',
            allow_anonymous_submissions=True,
            display_survey_directly=True,
            allow_multiple_submissions_per_user=True,
            thank_you_text='Thank you for taking the Personalisable Poll',
        )

        SurveysIndexPage.objects.first().add_child(instance=survey)
        survey.save_revision().publish()
        choices = ['next', 'end', 'survey']

        drop_down_field = PersonalisableSurveyFormField.objects.create(
            page=survey,
            sort_order=1,
            admin_label="where",
            label='Where should we go, in personsonalised style?',
            field_type='dropdown',
            skip_logic=skip_logic_data(choices),
            required=True,
            page_break=True
        )
        response = self.client.post(
            survey.url + '?p=1',
            {drop_down_field.clean_name: 'next'},
            follow=True,
        )
        self.assertContains(response, survey.thank_you_text)
        self.assertNotContains(response, 'That page number is less than 1')
