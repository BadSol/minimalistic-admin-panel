from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.apps import apps
import pytest
from django_fake_model import models as f  # Didin't manage to use it
from django.db import models
from min_admin.views import *
from min_admin.models import Person

"""
to test:
others:
putting min_admin to different url root
I can't test models

utils:
get_form
check_if_model_exist
crete_list_of_objects_with_attributes
get_model_name_and_model_obj_or_404
paginate
    can't test it for models
    test for model instances - ok

views:
model_list
    status_code 200 - ok
    display all of existing models - ok
object_list
    display correct data / 404 when model not found - ok
    redirect - ok
    displays objects - ok
object_detail
    display correct data / 404 when model/obj not found
object_delete
    get / post(delete obj)
object_create
    get / post(save obj)
object_update
    get / post(update obj)
"""


def test_assert_that_unauthorized_users_get_forwarded_to_login_page(client):
    response = client.get(reverse('min_admin:models'), follow=True)
    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/', 302)])


def test_model_list_view_as_authorized(admin_client):
    response = admin_client.get(reverse('min_admin:models'))
    assert(response.status_code == 200)


def test_model_list_view_lists_all_min_admin_models(admin_client):
    model_names = []
    for model in apps.get_app_config('min_admin').get_models():
        model_names.append(model._meta.verbose_name)

    response = admin_client.get(reverse('min_admin:models'))
    assert(all(model in response.content for model in model_names))


def test_object_list_view_as_unauthorized(client):
    response = client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}), follow=True)
    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/', 302)])


def test_object_list_view_as_authorized(admin_client):
    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert(response.status_code == 200)


def test_object_list_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'MissingNo'}))
    assert(response.status_code == 404)


def test_object_list_view_displaying_model_instances(admin_client):
    person = Person(first_name='First', last_name='Last')
    person.save()

    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert("First Last" in response.content)


def test_paginator_on_object_list_view(admin_client):
    for person in range(0, 16):  # todo: move pagination default to settings
        person_instance = Person(first_name=str(person), last_name='test')
        person_instance.save()

    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert(str(response.context['objects']) == '<Page 1 of 2>')




# class MinAdminApiViewTest(TestCase):
#     def setUp(self):
#         pass
#
#     def test_index_view_status_code_200(self):
#         response = self.client.get(reverse('min_admin:models'))
#         assert(response.status_code == 200)
#
#     def test_index_view_response_contain_model_names(self):
#         model_names = []
#         for model in apps.get_app_config('min_admin').get_models():
#             model_names.append(model._meta.verbose_name)
#
#         response = self.client.get(reverse('min_admin:models'))
#         assert(all(model in response.content for model in model_names))
#
#     def test_model_view_model_name_out_of_regex_bounds(self):
#         """ Assert NoReverseMatch exception when url doesn't much regular expression"""
#         with pytest.raises(NoReverseMatch):
#             self.client.get(reverse('min_admin:objectList', args=[21*'a']))


# def test_model_view_model_name_doesnt_exist(rf, admin_client):
#     # request = rf.get(reverse('min_admin:objectList', args=['nonexistingmodel']))
#     # request.client = admin_client
#     # request.user = 'test'
#     # response = object_list(request)
#     response = admin_client.get(reverse('min_admin:objectList', args=['nonexistingmodel']))
#     assert(response.status_code == 404)