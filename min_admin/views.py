from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
# from django.forms import ModelForm
# from django import forms
from django.forms.models import ModelForm
# from django.contrib import messages
# from django.contrib.admin.views.decorators import staff_member_required

# Utils:


from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def super_user_or_staff_member_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                          login_url='admin:login'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member or superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.is_staff or u.is_superuser),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def get_form(my_model, exclude_list):
    class MyForm(ModelForm):
        class Meta:
            model = my_model
            exclude = exclude_list
    return MyForm


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


def get_model_name_and_model_obj_or_404(model_name):
    """ returns model_name.lower() or raise 404 if model doesn't exist"""
    model_name = model_name.lower()
    if not check_if_model_exist(model_name):
        raise Http404("\"{}\" model doesn't exist".format(model_name.capitalize()))
    model = apps.get_app_config('min_admin').get_model(model_name)
    return model_name, model


# VIEWS:


@super_user_or_staff_member_required
def model_list(request):
    app_models = apps.get_app_config('min_admin').get_models()
    models = []
    for model in app_models:
        models.append(model._meta.verbose_name)

    context = {'models': models}
    return render(request, 'min_admin/main.html', context)


@super_user_or_staff_member_required
def object_list(request, model_name):
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    model_fields = model._meta.get_fields()
    objects = model.objects.all()
    context = {'objects': crete_list_of_objects_with_attributes(objects, model_fields),
               'fields': model_fields,
               'model_name': model_name}

    return render(request, 'min_admin/model_objects.html', context)


@super_user_or_staff_member_required
def object_detail(request, model_name, pk):
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    try:
        object_instance = model.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404("\"{}\" object doesn't exist".format(model_name.capitalize()))

    data = model_to_dict(object_instance)

    context = {'object': object_instance,
               'data': data.items(),
               'model_name': model_name.capitalize()}
    return render(request, 'min_admin/details.html', context)


@super_user_or_staff_member_required
def object_delete(request, model_name, pk):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404()

    model_name, model = get_model_name_and_model_obj_or_404(model_name)  # Making sure model exist
    model_instance = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        # delete model instance
        model_instance.delete()

        return redirect(reverse('min_admin:modelObjects', kwargs={'model_name': model_name}))

    context = {'object': model_instance,
               'model_name': model_name.capitalize()}
    return render(request, 'min_admin/delete.html', context)


@super_user_or_staff_member_required
def object_create(request, model_name):
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    form_model = get_form(model, [])

    form = form_model(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(reverse('min_admin:objectDetail', kwargs={'model_name': model_name, 'pk': instance.pk}))

    context = {'model_name': model_name,
               "form": form}
    return render(request, 'min_admin/create_object.html', context)


@super_user_or_staff_member_required
def object_update(request, model_name, pk):
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    instance = get_object_or_404(model, pk=pk)
    form_model = get_form(model, [])

    form = form_model(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect(reverse('min_admin:objectDetail', kwargs={'model_name': model_name, 'pk': instance.pk}))

    context = {'model_name': model_name,
               "form": form,
               "instance": instance}
    return render(request, 'min_admin/update_object.html', context)





