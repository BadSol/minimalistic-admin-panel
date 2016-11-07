from django.shortcuts import render, redirect, get_object_or_404
from django.apps import apps
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from min_admin.utils import super_user_or_staff_member_required, get_model_name_and_model_obj_or_404, \
    crete_list_of_objects_with_attributes, get_form, paginate


@super_user_or_staff_member_required
def model_list(request):
    page = request.GET.get('page', 1)
    app_models = apps.get_app_config('min_admin').get_models()
    models = []
    for model in app_models:
        models.append(model._meta.verbose_name)

    items = paginate(models, page)

    context = {'objects': items}
    return render(request, 'min_admin/main.html', context)


@super_user_or_staff_member_required
def object_list(request, model_name):
    page = request.GET.get('page', 1)
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    # model_fields = model._meta.get_fields()
    objects = model.objects.all()
    objects = crete_list_of_objects_with_attributes(objects)

    items = paginate(objects, page)

    context = {'objects': items,
               # 'fields': model_fields,
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
               'id': pk,
               'data': data.items(),
               'model_name': model_name.capitalize()}
    return render(request, 'min_admin/details.html', context)


@super_user_or_staff_member_required
def object_delete(request, model_name, pk):
    model_name, model = get_model_name_and_model_obj_or_404(model_name)  # Making sure model exist
    model_instance = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        model_instance.delete()

        return redirect(reverse('min_admin:objectList', kwargs={'model_name': model_name}))

    context = {'object': model_instance,
               'model_name': model_name.capitalize(),
               'id': pk}
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
               'id': pk,
               "form": form,
               "instance": instance}
    return render(request, 'min_admin/update_object.html', context)
