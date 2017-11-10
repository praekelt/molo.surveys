from django.conf import settings
from django.utils.html import format_html_join
from django.contrib.auth.models import User

from wagtail.contrib.modeladmin.options import modeladmin_register
from wagtail.wagtailcore import hooks

from molo.surveys.models import MoloSurveyPage, SurveyTermsConditions
from molo.core.models import ArticlePage

from .admin import SegmentUserGroupAdmin


modeladmin_register(SegmentUserGroupAdmin)


@hooks.register('construct_main_menu')
def show_surveys_entries_for_users_have_access(request, menu_items):
    if not request.user.is_superuser and not User.objects.filter(
            pk=request.user.pk, groups__name='Moderators').exists():
        menu_items[:] = [
            item for item in menu_items if item.name != 'surveys']


@hooks.register('insert_global_admin_js')
def global_admin_js():
    js_files = [
        'js/survey-admin.js',
    ]

    js_includes = format_html_join(
        '\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes


@hooks.register('after_copy_page')
def create_new_page_relations(request, page, new_page):
    if page and new_page:
        if new_page.get_descendants().count() >= \
                page.get_descendants().count():
            for survey in MoloSurveyPage.objects.descendant_of(
                    new_page.get_site().root_page):
                # replace old terms and conditions with new one, if it exists
                relations = SurveyTermsConditions.objects.filter(page=survey)
                for relation in relations:
                    if relation.terms_and_conditions:
                        new_article = ArticlePage.objects.descendant_of(
                            new_page.get_site().root_page).filter(
                                slug=relation.terms_and_conditions.slug)\
                            .first()
                        relation.terms_and_conditions = new_article
                        relation.save()
