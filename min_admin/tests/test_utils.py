import pytest
from min_admin.views import *
from min_admin.models import Person
from min_admin.utils import get_form, get_model_name_and_model_obj_or_404, check_if_model_exist, paginate


def test_get_model_name_and_model_obj_or_404_successful():
    model_name, model = get_model_name_and_model_obj_or_404('PERSON')

    assert(model_name == 'person' and str(model) == "<class 'min_admin.models.Person'>")


def test_get_model_name_and_model_obj_or_404_fail():

    with pytest.raises(Http404):
        get_model_name_and_model_obj_or_404('MissingModel')


def test_get_form():
    model_name = 'person'
    model_name, model = get_model_name_and_model_obj_or_404(model_name)
    form = get_form(model, [])

    assert(('fist_name' and 'last_name') in form.base_fields)


def test_check_if_model_exist_when_model_exist():
    assert(check_if_model_exist('person') == True)


def test_check_if_model_exist_when_model_doesnt_exist():
    assert(check_if_model_exist('MissingModel') == False)


@pytest.mark.django_db
def test_crete_list_of_objects_with_attributes():
    person = Person(first_name='test', last_name='person 1')
    person.save()
    person = Person(first_name='test', last_name='person 2')
    person.save()
    persons = Person.objects.all()

    result = (crete_list_of_objects_with_attributes(persons))
    expected_data = "[[<Person: test person 1>, [('first_name', u'test'), ('last_name', u'person 1'), (u'id', 1)]], " \
                    "[<Person: test person 2>, [('first_name', u'test'), ('last_name', u'person 2'), (u'id', 2)]]]"

    assert(str(result) == expected_data)


@pytest.mark.django_db
def test_paginate():
    person = Person(first_name='test', last_name='person 1')
    person.save()

    persons = Person.objects.all()
    objects = crete_list_of_objects_with_attributes(persons)

    result = paginate(data=objects, page=1)

    assert(str(result) == "<Page 1 of 1>")
