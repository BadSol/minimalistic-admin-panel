from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class MinAdminApiViewTest(TestCase):
    def test_index_view_status_code_200(self):
        response = self.client.get(reverse('index'))
        assert(response.status_code == 200)

    def test_index_view_response_contain_model_names(self):
        model_names = []
        for model in apps.get_app_config('min_admin').get_models():
            model_names.append(model._meta.verbose_name)

        response = self.client.get(reverse('index'))

        assert(all(model in response.content for model in model_names))

