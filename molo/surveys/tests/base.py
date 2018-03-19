from molo.surveys.models import (
    MoloSurveyFormField,
    MoloSurveyPage,
    SurveysIndexPage,
)
from .utils import skip_logic_data


def create_molo_survey_form_field(survey, sort_order, obj):
    if obj['type'] == 'radio':
        skip_logic = skip_logic_data(choices=obj['choices'])
    else:
        skip_logic = None

    return MoloSurveyFormField.objects.create(
        page=survey,
        sort_order=sort_order,
        label=obj["question"],
        field_type=obj["type"],
        required=obj["required"],
        page_break=obj["page_break"],
        admin_label=obj["question"].lower().replace(" ", "_"),
        skip_logic=skip_logic
    )


def create_molo_survey_page(
        parent, title="Test Survey", slug='test-survey', **kwargs):
    molo_survey_page = MoloSurveyPage(
        title=title, slug=slug,
        introduction='Introduction to Test Survey ...',
        thank_you_text='Thank you for taking the Test Survey',
        submit_text='survey submission text',
        **kwargs
    )

    parent.add_child(instance=molo_survey_page)
    molo_survey_page.save_revision().publish()

    return molo_survey_page


def create_survey(fields={}, **kwargs):
    survey = create_molo_survey_page(SurveysIndexPage.objects.first())

    if not fields == {}:
        num_questions = len(fields)
        for index, field in enumerate(reversed(fields)):
            sort_order = num_questions - (index + 1)
            create_molo_survey_form_field(survey, sort_order, field)
    return survey
