
from django.conf.urls import url
from molo.surveys.views import SurveySuccess, submission_article


urlpatterns = [
    url(
        r"^(?P<slug>[\w-]+)/success/$",
        SurveySuccess.as_view(),
        name="success"
    ),
    url(
        r'^submissions/(\d+)/article/(\d+)/$',
        submission_article, name='article'),
]
