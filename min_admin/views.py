from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.apps import apps


def index(request):
    app_models = apps.get_app_config('min_admin').get_models()
    model_names = ""

    for model in app_models:
        model_names += "[{}] ".format(model._meta.verbose_name)

    return HttpResponse("Existing models: " + model_names)
