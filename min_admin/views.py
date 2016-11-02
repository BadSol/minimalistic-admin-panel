from django.shortcuts import render
from django.apps import apps
from django.http import Http404
from models import Person, Teacher, Class


def index_view(request):
    app_models = apps.get_app_config('min_admin').get_models()
    models = []
    for model in app_models:
        models.append(model._meta.verbose_name)

    context = {'models': models}
    return render(request, 'min_admin/main.html', context)


def model_view(request, model_name):
    model_name = model_name.lower()

    if not check_if_model_exist(model_name):
        raise Http404("\"{}\" model doesn't exist".format(model_name))

    model = apps.get_app_config('min_admin').get_model(model_name)
    objects = model.objects.all()
    context = {'objects': objects}
    return render(request, 'min_admin/model_objects.html', context)


def check_if_model_exist(model_name):
    app_models = apps.get_app_config('min_admin').get_models()

    for model in app_models:
        if model_name == model._meta.verbose_name:
            return True
    return False
