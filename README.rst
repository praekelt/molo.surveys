molo.surveys
=============================

.. image:: https://img.shields.io/travis/praekelt/molo.surveys.svg
        :target: https://travis-ci.org/praekelt/molo.surveys

.. image:: https://img.shields.io/pypi/v/molo.surveys.svg
        :target: https://pypi.python.org/pypi/molo.surveys

.. image:: https://coveralls.io/repos/praekelt/molo.surveys/badge.png?branch=develop
    :target: https://coveralls.io/r/praekelt/molo.surveys?branch=develop
    :alt: Code Coverage

An implementation of wagtailsurveys as a Molo plugin

Installation::

   pip install molo.surveys


Django setup::

   INSTALLED_APPS = (
      'wagtailsurveys',
      'wagtail_personalisation',
      'wagtailfontawesome',

   )


In your urls.py::

    url(
        r"^(?P<slug>[\w-]+)/success/$",
        SurveySuccess.as_view(),
        name="success"
    ),


In your main.html::

   {% load molo_survey_tags %}

   {% block content %}
      {% surveys_list %}
   {% endblock %}

In your section page or article page::

   {% load molo_survey_tags %}

   {% block content %}
    {{% surveys_list_for_pages page=self %}
   {% endblock %}
