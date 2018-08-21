CHANGE LOG
==========

6.10.0
------
- Add the missing Migration
- Fix the typo in the models help_text causing "TypeError: ugettext()"

6.9.10
------
- Add error validation for choice fields

6.9.9
-----
- Decode items in csv download list

6.9.0
-----
- Override choice field to textfield from charfied with 512 limit

6.8.2
-----
- Bug Fix: redirect to translated surveys when another language is selected

6.8.1
-----
- Ensure translated surveys are also pulled through to the admin view

6.8.0
-----
- Remove hardcoded groups for displaying the surveys in wagtail menu

6.7.6
-----
- Bugfix: Ensure results of surveys, that are children of articles, pull through to the admin view

6.7.5
-----
- Bugfix: Handle errors when testing invalid rules
- Upgrade wagtail-personalisation-molo to 0.11.3

6.7.4
-----
- Upgrade wagtail-personalisation-molo to 0.11.2

6.7.3
-----
- Accept a wide range of date formats for date and datetime survey fields
- Run validation on default values for date and datetime form fields

6.7.2
-----
- Upgrade wagtail-personalisation-molo to 0.11.1

6.7.1
-----
- Bugfix: Fix skip logic handling of form errors
- Bugfix: Fix survey rules validation and user_info_strings

6.7.0
-----
- Add get_visit_count() for the PersistentSurveysSegmentsAdapter
- Add get_column_header() and get_user_info_string() for rules

6.6.2
-----
- Bugfix: only store one MoloSurveyPageView per page view
- Add management command to deduplicate pageview data

6.6.1
-----
- Add Homepage Introduction
- Reorder ContentPanels

6.6.0
-----
- Add personalisable_survey check to surveys list

6.5.0
-----
- Replace Page with MoloPage proxy

6.4.6
-----
- Upgrade wagtail-personalisation-molo to 0.10.6

6.4.5
-----
- Bug Fix: stop using private API self.build_attrs() on form fields

6.4.3
-----
- Bug Fix: Display Rule errors on Segment creation page when calculating the count

6.4.3
-----
- Template name: Rename SurveySuccess template name from molo_survey_page_landing to molo_survey_page_success

6.4.2
-----
- Bug Fix: Display errors for Segment creation form when calculating the count
- Bug Fix: Remove extra Positive Number survey field option

6.4.1
-----
- Bug Fix: Fix skipping required question when two questions are in one step and one is required

6.4.0
-----
- Add segment user count button to wagtail modeladmin create template and display the number of matched users
- Add View for counting how many users match a segments rules

6.3.2
-----
- Upgrade wagtail-personalisation-molo to 0.10.4

6.3.1
-----
- Bug Fix: Ensure segmentation rules are static

6.3.0
-----
- Add support for Python 3
- Improve templates

6.2.0
-----
- add support for Django 1.11

6.1.4
-----
- Bug Fix: Prevent 404 errors when attempting to access edit view on segments

6.1.3
-----
- Bug Fix: Include Include Survey Response Rule in Combination Rule

6.1.2
-----
- Bug Fix: Show form validation error when no redio button choice has been selected in skip logic

6.1.1
-----
- Minor improvement: Segments with ArticleTagRule using PersistentSurveysSegmentsAdapter now
  retrieve data from the model rather than the session.

6.1.0
-----
- New feature: PersistentSurveysSegmentsAdapter can be used instead of SurveysSegmentsAdapter to
  store ArticleTagRule data in a model.

6.0.0
-----
- Official release for Molo Surveys 6.0.0
- Dropped support for Django 1.10

6.0.0-beta.1
------------
- Upgrade to Django 1.0, Molo 6x

5.9.12
------
- Bug Fix: Fix csv headers and columns for personalisable surveys

5.9.11
------
- Bug Fix: Fix question order numbering

5.9.10
------
- Add page break setting
- Add different label for checkboxes instead of skip logic

5.9.9
-----
- Bug Fix: Issue with static wrapper

5.9.8
-----
- [ERROR]
- Intended changes not added to release

5.9.7
-----
- Add survey response rule
- Add character limits to multiline text inputs
- Bug Fix: Fix visitor rule not updating

5.9.6
-----
- Bug Fix: Tackle MultiValueKeyError exception when checkboxes answer is empty

5.9.5
-----
- Bug Fix: Make sure Comment Count Ruls is surface in Combination Rule

5.9.4
-----
- Bug Fix: Handle case where single nested logic block is given to the Combination Rule

5.9.3
-----
- Add admin label to survey questions

5.9.2
-----
- Added a filter to check if a form field is a checkbox

5.9.1
-----
- Bug Fix: Update wagtail-personalisation-molo which adds in collectstatic
- Change NestedBlocks to Nested Blocks in Admin UI
- Bug Fix:  Ensure that 'Add Rule Combination' button only appears when there is no Rule Combination
- Add description for how Rule Combination works

5.9.0
-----
- Added static and dynamic segments
- Changed dependency on wagtail personalisation to a forked version
- Update user privacy

5.8.2
--------
- Bug Fix: fixed string replacement bug in combination rule javascript

5.8.1
--------
- Fixed Combination Rule clean method for checking rule operator ordering
- Bug Fix: removed reference to non-existent migration

5.8.0
--------
- Added Combination Rule to allow combining rules within a segment
- Bug Fix: renamed migration

5.7.0
--------
- Added Article Tag Rule to allow segmenting on article visits
- Added ability to skip questions and surveys based on user's response

5.6.5
-----
- Bug Fix: get the correct index page for the correct site when converting YWC to an article

5.6.4
-----
- Bug Fix: add yourwords check to surveys list

5.6.3
-----
- Bug Fix: removed yourwords surveys from template and dismpay the number of matched users tag lists

5.6.2
-----
- Bug Fix: remove PreventDeleteMixin from Ts&Cs index page

5.6.1
-----
- Use FooterPage instead of ArticlePage for the Surveys Ts&Cs

5.6.0
-----
- Added Terms and Conditions index page and page relation to molo survey page
- Added image and body content to survey

5.5.0
-----
- Add advanced surveys

5.4.0
-----
- Add option to enter customised homepage button text

5.3.0
-----
- Add option to convert survey submission to an article

5.2.1
-----
- Add option to show results as percentage
- Add option to enter customised submit text

5.2.0
-----
- Add templatetags filters for direct and linked surveys

5.1.0
-----
- Add poll like functionality

5.0.1
-----
- Bug Fix: Filter by id for site specific surveys

5.0.0
-----
- Added merged cms functionality to surveys
- Only able to see relevant surveys for site in admin and csv

2.3.0
-----
- Add a success url after user submit answers to a survey

2.2.2
-----
- Create a success page after user submit answers to a survey

2.2.1
-----
- Bug Fix: Survey model inherited from non routable page mixin

2.2.0
-----
- Added Surveys headline template and dismpay the number of matched users tag and Surveys headline template and dismpay the number of matched users file for footer headline link

2.1.0
-----
- Removed ability to delete Surveys IndexPage in the Admin UI

2.0.0
-----
- Upgraded dependency to molo v4

1.2.3
-----
- Add surveys permissions to groups

1.2.2
-----
- Return None if there is no survey

1.2.1
-----
- Make sure when submitting numbers in a number field it gets stored in the correct format

1.2.0
-----
- Add support for hiding untranslated content

1.1.0
-----
- Adding BEM rules to the template and dismpay the number of matched users

1.0.0
-----
- Added multi-language support

NOTE: This release is not compatible with Molo versions that are less than 3.0

0.1.0
-----
- Initial commit
