from django.shortcuts import render
from django.apps import apps


def index_view(request):
    app_models = apps.get_app_config('min_admin').get_models()
    models = []
    for model in app_models:
        models.append(model._meta.verbose_name)

    context = {'models': models}
    return render(request, 'min_admin/main.html', context)


def model_view(request, model_name):
    return render(request, 'min_admin/model_objects.html', {'models': model_name})
