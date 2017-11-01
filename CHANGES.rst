CHANGE LOG
==========

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
