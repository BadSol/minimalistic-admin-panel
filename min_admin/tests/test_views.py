from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.apps import apps
import pytest


class MinAdminApiViewTest(TestCase):
    def test_index_view_status_code_200(self):
        response = self.client.get(reverse('min_admin:models'))
        assert(response.status_code == 200)

    def test_index_view_response_contain_model_names(self):
        model_names = []
        for model in apps.get_app_config('min_admin').get_models():
            model_names.append(model._meta.verbose_name)

        response = self.client.get(reverse('min_admin:models'))
        assert(all(model in response.content for model in model_names))

    def test_model_view_model_name_out_of_regex_bounds(self):
        """ Assert NoReverseMatch exception when url doesn't much regular expression"""
        with pytest.raises(NoReverseMatch):
            self.client.get(reverse('min_admin:objectList', args=[21*'a']))

    def test_model_view_model_name_doesnt_exist(self):
        response = self.client.get(reverse('min_admin:objectList', args=['nonexistingmodel']))
        assert(response.status_code == 404)
