import pytest
from min_admin.views import *
from min_admin.models import Person
"""
to test:
others:
putting min_admin to different url root
I can't test models

views:
model_list
    status_code 200 - ok
    display all of existing models - ok
object_list
    display correct data / 404 when model not found - ok
    redirect - ok
    displays objects - ok
    paginate - ok
object_detail
    status code - ok
    forward - ok
    display correct data - ok
    404 when model/obj not found -ok
object_create
    get / post(save obj) - all ok
object_delete
    get / post(delete obj) - all ok
object_update
    get / post(update obj) - all ok
    displays correct data - ok
"""


def test_assert_that_unauthorized_users_get_forwarded_to_login_page(client):
    response = client.get(reverse('min_admin:models'), follow=True)
    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/', 302)])


def test_model_list_view_as_authorized(admin_client):
    response = admin_client.get(reverse('min_admin:models'))
    assert(response.status_code == 200)


def test_model_list_view_lists_all_min_admin_models(admin_client):
    model_names = []
    for model in apps.get_app_config('min_admin').get_models():
        model_names.append(model._meta.verbose_name)

    response = admin_client.get(reverse('min_admin:models'))
    assert(all(model in response.content for model in model_names))


def test_object_list_view_as_unauthorized(client):
    response = client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}), follow=True)
    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/', 302)])


def test_object_list_view_as_authorized(admin_client):
    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert(response.status_code == 200)


def test_object_list_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'MissingNo'}))
    assert(response.status_code == 404)


def test_object_list_view_displaying_model_instances(admin_client):
    person = Person(first_name='First', last_name='Last')
    person.save()

    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert("First Last" in response.content)


def test_paginator_on_object_list_view(admin_client):
    for person in range(0, 16):  # todo: move pagination default objects per page to settings
        person_instance = Person(first_name=str(person), last_name='test')
        person_instance.save()

    response = admin_client.get(reverse('min_admin:objectList', kwargs={'model_name': 'person'}))
    assert(str(response.context['objects']) == '<Page 1 of 2>')


@pytest.mark.django_db
def test_object_detail_view_as_unauthorized(client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = client.get(reverse('min_admin:objectDetail', kwargs={'model_name': 'person',
                                                                    'pk': pk}), follow=True)

    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/{}/'.format(pk), 302)])


def test_object_detail_view_as_authorized(admin_client):
    person = Person(first_name='First', last_name='Last')  # todo: DRY
    person.save()
    pk = person._get_pk_val()

    response = admin_client.get(reverse('min_admin:objectDetail', kwargs={'model_name': 'person',
                                                                          'pk': pk}))

    assert(response.status_code == 200)


def test_object_detail_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectDetail', kwargs={'model_name': 'MissingModel',
                                                                          'pk': 1}))

    assert(response.status_code == 404)


def test_object_detail_view_as_authorized_nonexistent_model_instance(admin_client):
    response = admin_client.get(reverse('min_admin:objectDetail', kwargs={'model_name': 'person',
                                                                          'pk': 1}))

    assert(response.status_code == 404)


def test_object_detail_view_displaying_correct_data(admin_client):
    person = Person(first_name='First', last_name='Last')  # todo: DRY
    person.save()
    pk = person._get_pk_val()

    expected_data = ['first_name: {}'.format(person.first_name),
                     'last_name: {}'.format(person.last_name),
                     'id: {}'.format(pk)]

    response = admin_client.get(reverse('min_admin:objectDetail', kwargs={'model_name': 'person',
                                                                          'pk': pk}))

    assert(all(fields in response.content for fields in expected_data))


def test_object_create_view_as_unauthorized(client):
    response = client.get(reverse('min_admin:objectCreate', kwargs={'model_name': 'person'}), follow=True)

    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/create/', 302)])


def test_object_create_view_as_authorized(admin_client):
    response = admin_client.get(reverse('min_admin:objectCreate', kwargs={'model_name': 'person'}))

    assert(response.status_code == 200)


def test_object_create_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectCreate', kwargs={'model_name': 'MissingModel'}))

    assert(response.status_code == 404)


def test_object_create_view_creating_object_instance(admin_client):
    first_name = 'test_first_name'
    last_name = 'test_last_name'
    admin_client.post(reverse('min_admin:objectCreate', kwargs={'model_name': 'person'}),
                      {'first_name': first_name,
                       'last_name': last_name})

    assert (first_name and last_name) in str(Person.objects.get())


@pytest.mark.django_db
def test_object_update_view_as_unauthorized(client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = client.get(reverse('min_admin:objectEdit', kwargs={'model_name': 'person', 'pk': pk}), follow=True)

    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/{}/edit/'.format(pk), 302)])


def test_object_update_view_as_authorized(admin_client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = admin_client.get(reverse('min_admin:objectEdit', kwargs={'model_name': 'person', 'pk': pk}))

    assert(response.status_code == 200)


def test_object_update_view_displaying_correct_data(admin_client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = admin_client.get(reverse('min_admin:objectEdit', kwargs={'model_name': 'person', 'pk': pk}))

    assert((person.first_name and person.last_name) in response.content)


def test_object_update_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectEdit', kwargs={'model_name': 'MissingModel', 'pk': 1}))

    assert(response.status_code == 404)


def test_object_update_view_as_authorized_nonexistent_model_instance(admin_client):
    response = admin_client.get(reverse('min_admin:objectEdit', kwargs={'model_name': 'person', 'pk': 1}))

    assert(response.status_code == 404)


def test_object_update_view_updating_object_instance(admin_client):
    person = Person(first_name='FN_before', last_name='LN_before')
    person.save()
    pk = person._get_pk_val()

    first_name_after = 'FN_after'
    last_name_after = 'LN_after'

    admin_client.post(reverse('min_admin:objectEdit', kwargs={'model_name': 'person', 'pk': pk}),
                      {'first_name': first_name_after,
                       'last_name': last_name_after})

    assert (first_name_after and last_name_after) in str(Person.objects.get())


@pytest.mark.django_db
def test_object_delete_view_as_unauthorized(client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = client.get(reverse('min_admin:objectDelete', kwargs={'model_name': 'person', 'pk': pk}), follow=True)

    assert(response.redirect_chain == [('/admin/login/?next=/min_admin/person/{}/delete/'.format(pk), 302)])


def test_object_delete_view_as_authorized(admin_client):
    person = Person(first_name='First', last_name='Last')
    person.save()
    pk = person._get_pk_val()

    response = admin_client.get(reverse('min_admin:objectDelete', kwargs={'model_name': 'person', 'pk': pk}))

    assert(response.status_code == 200)


def test_object_delete_view_as_authorized_nonexistent_model(admin_client):
    response = admin_client.get(reverse('min_admin:objectDelete', kwargs={'model_name': 'MissingModel', 'pk': 1}))

    assert(response.status_code == 404)


def test_object_delete_view_as_authorized_nonexistent_model_instance(admin_client):
    response = admin_client.get(reverse('min_admin:objectDelete', kwargs={'model_name': 'person', 'pk': 1}))

    assert(response.status_code == 404)


def test_object_delete_view_deleting_object_instance(admin_client):
    person = Person(first_name='Test', last_name='Person')
    person.save()
    pk = person._get_pk_val()

    admin_client.post(reverse('min_admin:objectDelete', kwargs={'model_name': 'person', 'pk': pk}))

    with pytest.raises(ObjectDoesNotExist):
        Person.objects.get(pk=pk)
