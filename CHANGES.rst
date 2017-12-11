CHANGE LOG
==========

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
- Bug Fix: removed yourwords surveys from template tag lists

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
- Added Surveys headline template tag and Surveys headline template file for footer headline link

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
- Adding BEM rules to the template

1.0.0
-----
- Added multi-language support

NOTE: This release is not compatible with Molo versions that are less than 3.0

0.1.0
-----
- Initial commit
