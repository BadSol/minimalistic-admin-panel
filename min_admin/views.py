from django.shortcuts import render
from django.apps import apps
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.core import serializers
# Utils:


def check_if_model_exist(model_name):
    app_models = apps.get_app_config('min_admin').get_models()

    for model in app_models:
        if model_name == model._meta.verbose_name:
            return True
    return False


def crete_list_of_objects_with_attributes(objects, model_fields):
    """
    prepares a list of object data lists in which each list contains instance of model object and all of its attributes
    for the sake of displaying object details
    """
    result = []
    for obj in objects:
        result.append([obj, model_to_dict(obj).items()])

    return result


def get_model_name_or_404(model_name):
    """ returns model_name.lower() or raise 404 if model doesn't exist"""
    model_name = model_name.lower()

    if not check_if_model_exist(model_name):
        raise Http404("\"{}\" model doesn't exist".format(model_name))
    return model_name


# VIEWS:


def index_view(request):
    app_models = apps.get_app_config('min_admin').get_models()
    models = []
    for model in app_models:
        models.append(model._meta.verbose_name)

    context = {'models': models}
    return render(request, 'min_admin/main.html', context)


def model_view(request, model_name):
    model_name = get_model_name_or_404(model_name)

    model = apps.get_app_config('min_admin').get_model(model_name)
    model_fields = model._meta.get_fields()
    objects = model.objects.all()
    context = {'objects': crete_list_of_objects_with_attributes(objects, model_fields),
               'fields': model_fields,
               'model_name': model_name}

    return render(request, 'min_admin/model_objects.html', context)


def detail_view(request, model_name, pk):
    model_name = get_model_name_or_404(model_name)
    model = apps.get_app_config('min_admin').get_model(model_name)
    try:
        object_instance = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404("\"{}\" object doesn't exist".format(model_name))

    data = model_to_dict(object_instance)

    context = {'object': object_instance,
               'data': data.items(),
               'model_name': model_name.capitalize()}
    return render(request, 'min_admin/details.html', context)
