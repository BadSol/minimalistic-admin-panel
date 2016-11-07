from django.apps import apps
from django.http import Http404
from django.forms.models import model_to_dict, ModelForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_form(my_model, exclude_list):
    """
    creates ModelForm based on model object
    :param my_model: Any model added to app models
    :param exclude_list: List of fields, that should be excluded from created form. In case of this project its easier
    and faster to pass empty list as argument, than get and format model fields just to pass it here
    :return: ModelForm form object
    """
    class MyForm(ModelForm):
        class Meta:
            model = my_model
            exclude = exclude_list
    return MyForm


def check_if_model_exist(model_name):  # todo: merge into get_model_name_and_model_obj_or_404 method

    app_models = apps.get_app_config('min_admin').get_models()

    for model in app_models:
        if model_name == model._meta.verbose_name:
            return True
    return False


def crete_list_of_objects_with_attributes(objects):
    """
    converts list of objects into a list of object dictionaries
    """
    result = []
    for obj in objects:
        result.append([obj, model_to_dict(obj).items()])

    return result


def get_model_name_and_model_obj_or_404(model_name):
    """ returns model_name.lower() or raise 404 if model doesn't exist
    :param model_name: model name passed from url
    :return: model_name and model.
    """
    model_name = model_name.lower()
    if not check_if_model_exist(model_name):
        raise Http404("\"{}\" model doesn't exist".format(model_name.capitalize()))
    model = apps.get_app_config('min_admin').get_model(model_name)
    return model_name, model


def paginate(data, page, items_per_page=15):
    """
    This method creates data for pagination
    """
    paginator = Paginator(data, items_per_page)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return items


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