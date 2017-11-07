from collections import defaultdict
import datetime

from wagtail_personalisation.adapters import SessionSegmentsAdapter
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from molo.core.models import ArticlePage
from .rules import CombinationRule


def get_rule(rule_hash, data_structure):
    rule_type, order = rule_hash.split('_')
    return data_structure[rule_type][int(order)]


def index_rules_by_type(rules):
    '''
    Indexes a list of rules by type name,
    while maintaining rule order for each rule type

    Sample Input:
    [
        <TimeRule: Time Rule>,
        <TimeRule: Time Rule>,
        <UserIsLoggedInRule: Logged in Rule>
    ]

    Sample Output:
    {
        'TimeRule': [ <TimeRule: Time Rule>, <TimeRule: Time Rule> ],
        'UserIsLoggedInRule': [ <UserIsLoggedInRule: Logged in Rule> ]
    }
    '''
    indexed_rules = {}
    for rule in rules:
        type_name = type(rule).__name__
        if type_name in indexed_rules:
            indexed_rules[type_name].append(rule)
        else:
            indexed_rules[type_name] = [rule]
    return indexed_rules


def transform_into_boolean_list(stream_data, indexed_rules, request):
    '''
    Converts a stream field of strings and rules into a list
    of booleans (evaluated rule evaluations), strings and nested lists

    Sample Input:
    [
        {u'type': u'Rule', u'value': u'UserIsLoggedInRule_0'},
        {u'type': u'Operator', u'value': u'and'},
        {u'type': u'NestedLogic', u'value': {
            u'operator': u'or',
            u'rule_1': u'TimeRule_0',
            u'rule_2': u'TimeRule_1'}
        }
    ]

    Output:
    [True, 'and', [False, 'or', True]]
    '''
    return_value = []
    for block in stream_data:
        if block['type'] == 'Rule':
            rule = get_rule(block['value'], indexed_rules)
            return_value.append(rule.test_user(request))
        elif block['type'] == 'Operator':
            return_value.append(block['value'])
        elif block['type'] == 'NestedLogic':
            values = block['value']
            rule_1 = get_rule(values['rule_1'], indexed_rules)
            rule_2 = get_rule(values['rule_2'], indexed_rules)
            return_value.append([
                rule_1.test_user(request),
                values['operator'],
                rule_2.test_user(request)
            ])

    return return_value


def evaluate(list_):
    '''
    Function that evaluates a list of boolean values
    seperated by strings that represent boolean values
    i.e. 'and', 'or'

    Sample Input:

    '''
    if len(list_) == 3:
        operator = list_[1]
        first = list_[0] if isinstance(list_[0], bool) else evaluate(list_[0])
        second = list_[2] if isinstance(list_[2], bool) else evaluate(list_[2])
        if operator == 'or':
            return first or second
        else:
            return first and second
    else:
        return evaluate([evaluate(list_[:3])] + list_[3:])


class SurveysSegmentsAdapter(SessionSegmentsAdapter):
    def add_page_visit(self, page):
        super(SurveysSegmentsAdapter, self).add_page_visit(page)
        tag_visits = self.request.session.setdefault(
            'tag_count',
            defaultdict(dict),
        )
        if isinstance(page.specific, ArticlePage):
            # Set the datetime based on UTC
            visit_time = datetime.datetime.now(timezone.utc).isoformat()
            for nav_tag in page.nav_tags.all():
                tag_visits.setdefault(str(nav_tag.tag.id), dict())
                tag_visits[str(nav_tag.tag.id)][page.path] = visit_time

    def get_tag_count(self, tag, date_from=None, date_to=None):
        """Return the number of visits on the given page"""
        if not date_from:
            date_from = timezone.make_aware(
                datetime.datetime.min,
                timezone.utc,
            )
        if not date_to:
            date_to = timezone.make_aware(
                datetime.datetime.max,
                timezone.utc,
            )

        tag_visits = self.request.session.setdefault(
            'tag_count',
            defaultdict(dict),
        )

        visits = tag_visits.get(str(tag.id), dict())
        valid_visits = [visit for visit in visits.values()
                        if date_from <= parse_datetime(visit) <= date_to]
        return len(valid_visits)

    def _test_rules(self, rules, request, match_any=False):
        if not rules:
            return False

        bool_rules = False
        bool_rules = [rule for rule in rules
                      if isinstance(rule, CombinationRule)]

        if not bool_rules:
            if match_any:
                return any(rule.test_user(request) for rule in rules)
            return all(rule.test_user(request) for rule in rules)
        else:
            # evaluates only 1 rule
            rule_combo = bool_rules[0]

            simple_rules = [rule for rule in rules
                            if not isinstance(rule, CombinationRule)]

            rules_indexed_by_type_name = index_rules_by_type(simple_rules)

            nested_list_of_booleans = transform_into_boolean_list(
                rule_combo.body.stream_data,
                rules_indexed_by_type_name,
                request
            )

            return evaluate(nested_list_of_booleans)
