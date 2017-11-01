from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

from molo.core.models import SiteLanguageRelation, Main, Languages, ArticlePage
from molo.core.tests.base import MoloTestCaseMixin
from molo.surveys.models import (MoloSurveyPage, MoloSurveyFormField,
                                 SurveysIndexPage)


User = get_user_model()


class TestSurveyAdminViews(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.client = Client()
        self.mk_main()
        self.main = Main.objects.all().first()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)
        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)
        self.french = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='fr',
            is_active=True)

        self.section = self.mk_section(self.section_index, title='section')
        self.article = self.mk_article(self.section, title='article')

        # Create surveys index pages
        self.surveys_index = SurveysIndexPage.objects.child_of(
            self.main).first()

        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')
        self.super_user = User.objects.create_superuser(
            username='testuser', password='password', email='test@email.com')

    def create_molo_survey_page(self, parent, **kwargs):
        molo_survey_page = MoloSurveyPage(
            title='Test Survey', slug='test-survey',
            intro='Introduction to Test Survey ...',
            thank_you_text='Thank you for taking the Test Survey',
            **kwargs
        )

        parent.add_child(instance=molo_survey_page)
        molo_survey_page.save_revision().publish()
        molo_survey_form_field = MoloSurveyFormField.objects.create(
            page=molo_survey_page,
            sort_order=1,
            label='Your favourite animal',
            field_type='singleline',
            required=True
        )
        return molo_survey_page, molo_survey_form_field

    def test_convert_to_article(self):
        molo_survey_page, molo_survey_form_field = \
            self.create_molo_survey_page(parent=self.section_index)

        self.client.login(username='tester', password='tester')
        response = self.client.get(molo_survey_page.url)
        self.assertContains(response, molo_survey_page.title)
        self.assertContains(response, molo_survey_page.intro)
        self.assertContains(response, molo_survey_form_field.label)
        response = self.client.post(molo_survey_page.url, {
            molo_survey_form_field.label.lower().replace(' ', '-'): 'python'
        }, follow=True)
        self.client.logout()
        self.client.login(
            username='testuser',
            password='password'
        )

        # test shows convert to article button when no article created yet
        response = self.client.get(
            '/admin/surveys/submissions/%s/' % molo_survey_page.id)
        self.assertContains(response, 'Convert to Article')

        # convert submission to article
        SubmissionClass = molo_survey_page.get_submission_class()

        submission = SubmissionClass.objects.filter(
            page=molo_survey_page).first()
        response = self.client.get(
            '/surveys/submissions/%s/article/%s/' % (
                molo_survey_page.id, submission.pk))
        self.assertEquals(response.status_code, 302)
        article = ArticlePage.objects.last()
        submission = SubmissionClass.objects.filter(
            page=molo_survey_page).first()
        self.assertEquals(article.title, article.slug)
        self.assertEquals(submission.article_page, article)
        self.assertEquals(article.body.stream_data, [
            {u"type": u"paragraph", u"value": u'tester'},
            {u"type": u"paragraph", u"value": u'python'},
            {u"type": u"paragraph", u"value": str(submission.created_at)}
        ])

        # first time it goes to the move page
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/move/' % article.id)

        # second time it should redirect to the edit page
        response = self.client.get(
            '/surveys/submissions/%s/article/%s/' % (
                molo_survey_page.id, submission.pk))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            response['Location'],
            '/admin/pages/%d/edit/' % article.id)
        response = self.client.get(
            '/admin/surveys/submissions/%s/' % molo_survey_page.id)

        # it should not show convert to article as there is already article
        self.assertNotContains(response, 'Convert to Article')
