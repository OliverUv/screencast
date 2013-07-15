# coding=UTF-8
import json

from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.test.client import Client

import models
from account.common import http_success


def object_count(object_type):
    return object_type.objects.all().count()


def preserve_count(object_type):
    def real_decorator(function):
        def wrapper(self, *args, **kwargs):
            objects = object_count(object_type)
            function(self, *args, **kwargs)
            self.assertEqual(objects, object_count(object_type))
        return wrapper
    return real_decorator


def diff_count(object_type, diff):
    def real_decorator(function):
        def wrapper(self, *args, **kwargs):
            objects = object_count(object_type)
            function(self, *args, **kwargs)
            self.assertEqual(diff, object_count(object_type) - objects)
        return wrapper
    return real_decorator


def create_user(name=None):
    user_id = User.objects.all().count() + 1
    username = 'user %s' % user_id
    if name:
        username = name
    password = 'pass'
    user = User.objects.create_user(username, '%s@test.com' % user_id, password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    # p = user.profile
    # p.postal_number = 58434
    # p.phone_number = 0720226044
    # p.full_name = 'boop derpatron'
    # p.save()

    return user


def add_test_data():
    users = [create_user() for _ in range(20)]

    groups = {
        'group0': (users[0], [users[1], users[2], users[3]]),
        'group1': (users[4], [users[5], users[6], users[7]])
    }

    for name, group_members in groups.iteritems():
        group = models.create_group(name, group_members[0])
        for u in group_members[1]:
            u.groups.add(group)

    return {
        'users': users,
        'groups': groups
    }


class HandyTestCase(TestCase):
    def assert_http_success(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, http_success().content)

    def assert_exists(self, query):
        self.assertTrue(query.exists())

    def assert_http_bad_request(self, response, substring=None):
        self.assertEqual(response.status_code, 400)
        parsed_response = json.loads(response.content)
        self.assertEqual(parsed_response['status'], 'failed')
        if substring:
            self.assertTrue(substring in parsed_response['message'])

    def create_users_and_fill_groups(self, groups_users, non_group_users):
        all_groups = groups_users.keys()
        all_users = set()
        for u in non_group_users:
            all_users.add(u)
        for group, group_members in groups_users.iteritems():
            for u in group_members:
                all_users.add(u)

        users = {}
        for u in all_users:  # Create all users
            users[u] = create_user(u)
        for g in all_groups:  # Create groups and add the users to them
            group = models.create_group(g, self.user)
            for u in groups_users[g]:
                users[u].groups.add(group)


class GeneralTests(HandyTestCase):
    def setUp(self):
        # Set up test data and log in our test user
        self.test_data = add_test_data()
        self.client = Client()
        self.user = self.test_data['users'][0]
        logged_in = self.client.login(username=self.user.username, password='pass')
        self.assertTrue(logged_in)

    @diff_count(Group, 1)
    def test_new_group_one_user(self):
        group_name = 'newgrouponeusertestgn'
        user_name = self.test_data['users'][1].username

        response = self.client.post('/account/groups/create_group/', {
            'groupname': group_name,
            'users': [user_name]
        })
        self.assert_http_success(response)
        self.assert_exists(Group.objects.filter(name=group_name, creator=self.user, observers=self.user))
        self.assert_exists(User.objects.filter(username=user_name, groups__name=group_name))

    @diff_count(Group, 1)
    def test_new_group_multiple_users(self):
        group_name = 'newgrouponeusertestgn'
        user_names = [u.username for u in self.test_data['users'][1:]]  # Add all users but the first

        response = self.client.post('/account/groups/create_group/', {
            'groupname': group_name,
            'users': user_names
        })
        self.assert_http_success(response)
        self.assert_exists(Group.objects.filter(name=group_name, creator=self.user, observers=self.user))
        for user_name in user_names:
            self.assert_exists(User.objects.filter(username=user_name, groups__name=group_name))

    @preserve_count(Group)
    def test_create_group_fail_no_group_name(self):
        user_name = self.test_data['users'][1].username

        response = self.client.post('/account/groups/create_group/', {
            'groupname': '',
            'users': [user_name]
        })
        self.assert_http_bad_request(response)

    @preserve_count(Group)
    def test_create_group_fail_not_post(self):
        user_name = self.test_data['users'][1].username

        response = self.client.get('/account/groups/create_group/', {
            'groupname': 'dingdings',
            'users': [user_name]
        })
        self.assert_http_bad_request(response, 'POST')

    def test_completion_only_users(self):
        groups_users = {
            'dong0': ['binu0', 'binu1', 'bbbbb'],
            'dong1': ['binu0', 'binu2', 'binu3', 'binu4', 'ddddd', 'ccccc'],
            'dong2': []
        }
        non_group_users = ['binu5', 'xaxax']
        completion_string = 'bin'
        completed_names = ['binu0', 'binu1', 'binu2', 'binu3', 'binu4', 'binu5']

        self.create_users_and_fill_groups(groups_users, non_group_users)

        expected_names = [{'value': n, 'category': ''} for n in completed_names]
        expected_groups = []
        expected_result = expected_names + expected_groups

        response = self.client.get('/account/complete_users_and_groups/%s/' % completion_string)
        self.assertEqual(response.status_code, 200)
        parsed_response = json.loads(response.content)
        self.assertItemsEqual(parsed_response, expected_result)

    def test_completion_groups_and_users(self):
        groups_users = {
            'bing0': ['binu0', 'binu1', 'aaaaa'],
            'dong0': ['binu0', 'binu1', 'bbbbb'],
            'bing1': ['binu0', 'binu2', 'binu3', 'binu4', 'ccccc'],
            'dong1': ['binu0', 'binu2', 'binu3', 'binu5', 'ddddd', 'ccccc'],
            'bing2': [],
            'dong2': []
        }
        non_group_users = ['binu6', 'eeeee']
        completion_string = 'bin'
        completed_names = ['binu0', 'binu1', 'binu2', 'binu3', 'binu4', 'binu5', 'binu6']
        completed_groups = ['bing0', 'bing1', 'bing2']

        expected_names = [{'value': n, 'category': ''} for n in completed_names]
        expected_groups = [{
            'value': g,
            'category': 'groups',
            'members': groups_users[g]}
            for g in completed_groups]
        expected_result = expected_names + expected_groups

        self.create_users_and_fill_groups(groups_users, non_group_users)

        response = self.client.get('/account/complete_users_and_groups/%s/' % completion_string)
        self.assertEqual(response.status_code, 200)
        parsed_response = json.loads(response.content)

        self.assertItemsEqual(parsed_response, expected_result)

    def test_completion_only_groups(self):
        groups_users = {
            'bing0': ['aaaaa', 'zzzzz', 'ccccc'],
            'bing1': ['aaaaa', 'ddddd', 'xxxxx'],
            'dong0': ['wwwww', 'ddddd', 'ccccc']
        }
        non_group_users = ['fffff', 'eeeee']
        completion_string = 'bin'
        completed_groups = ['bing0', 'bing1']

        expected_names = []
        expected_groups = [{
            'value': g,
            'category': 'groups',
            'members': groups_users[g]}
            for g in completed_groups]
        expected_result = expected_names + expected_groups

        self.create_users_and_fill_groups(groups_users, non_group_users)

        response = self.client.get('/account/complete_users_and_groups/%s/' % completion_string)
        self.assertEqual(response.status_code, 200)
        parsed_response = json.loads(response.content)

        self.assertItemsEqual(parsed_response, expected_result)
