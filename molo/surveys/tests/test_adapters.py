from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.test.client import Client

from wagtail_personalisation.rules import UserIsLoggedInRule

from molo.core.models import Main
from molo.core.tests.base import MoloTestCaseMixin

from molo.surveys.adapters import (
    get_rule,
    index_rules_by_type,
    transform_into_boolean_list,
    evaluate,
)
from molo.surveys.models import SegmentUserGroup

from molo.surveys.rules import GroupMembershipRule


class TestAdapterUtils(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.client = Client()
        self.mk_main()
        self.main = Main.objects.all().first()

        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')
        self.request.user = get_user_model().objects.create_user(
            username='tester', email='tester@example.com', password='tester')

        self.group_1 = SegmentUserGroup.objects.create(name='Group 1')
        self.group_2 = SegmentUserGroup.objects.create(name='Group 2')

        self.request.user.segment_groups.add(self.group_1)

    def test_get_rule(self):
        fake_ds = {
            'TimeRule': ['first time rule', 'second time rule'],
            'UserIsLoggedInRule': ['first logged in rule']
        }

        self.assertEqual(get_rule('TimeRule_0', fake_ds),
                         fake_ds["TimeRule"][0])
        self.assertEqual(get_rule('TimeRule_1', fake_ds),
                         fake_ds["TimeRule"][1])
        self.assertEqual(get_rule('UserIsLoggedInRule_0', fake_ds),
                         fake_ds["UserIsLoggedInRule"][0])

    def test_index_rules_by_type(self):
        group_rule_1 = GroupMembershipRule(group=self.group_1)
        group_rule_2 = GroupMembershipRule(group=self.group_2)
        logged_in_rule = UserIsLoggedInRule(is_logged_in=True)

        test_input = [logged_in_rule, group_rule_1, group_rule_2]
        expected_output = {
            'GroupMembershipRule': [group_rule_1, group_rule_2],
            'UserIsLoggedInRule': [logged_in_rule]
        }

        self.assertEqual(
            index_rules_by_type(test_input),
            expected_output)

    def test_transform_into_boolean_list_simple(self):
        group_rule_1 = GroupMembershipRule(group=self.group_1)
        group_rule_2 = GroupMembershipRule(group=self.group_2)
        logged_in_rule = UserIsLoggedInRule(is_logged_in=True)

        sample_stream_data = [
            {u'type': u'Rule', u'value': u'UserIsLoggedInRule_0'},
            {u'type': u'Operator', u'value': u'and'},
            {
                u'type': u'NestedLogic',
                u'value': {
                    u'operator': u'or',
                    u'rule_1': u'GroupMembershipRule_0',
                    u'rule_2': u'GroupMembershipRule_1'}
            }
        ]

        sample_indexed_rules = {
            'GroupMembershipRule': [group_rule_1, group_rule_2],
            'UserIsLoggedInRule': [logged_in_rule]
        }

        self.assertEqual(
            transform_into_boolean_list(
                sample_stream_data,
                sample_indexed_rules,
                self.request
            ),
            [logged_in_rule.test_user(self.request),
             u'and',
             [
                group_rule_1.test_user(self.request),
                u'or',
                group_rule_2.test_user(self.request)
            ]]
        )

    def test_evaluate_1(self):
        self.assertEqual(
            (False or True),
            evaluate([False, "or", True])
        )

    def test_evaluate_2(self):
        self.assertEqual(
            (False and True or True),
            evaluate([False, "and", True, "or", True])
        )

    def test_evaluate_3(self):
        self.assertEqual(
            (False and True),
            evaluate([False, "and", True])
        )

    def test_evaluate_4(self):
        self.assertEqual(
            ((False or True) and True),
            evaluate([[False, "or", True], "and", True])
        )

    def test_evaluate_5(self):
        self.assertEqual(
            ((False or True) and (False and False)),
            evaluate([[False, "or", True], "and", [False, "and", False]])
        )

    def test_evaluate_6(self):
        self.assertEqual(
            ((False or
                (True or False)) and
             (False and False)),
            evaluate(
                [[False, "or",
                    [True, "or", False]], "and",
                 [False, "and", False]])
        )

    def test_evaluate_7(self):
        self.assertEqual(
            ((False or True) and
             (False and False) or
             (True and False)),
            evaluate(
                [[False, "or", True], "and",
                 [False, "and", False], "or",
                 [True, 'and', False]])
        )
