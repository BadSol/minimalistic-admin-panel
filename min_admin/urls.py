from django.conf.urls import url
import views

app_name = 'min_admin'
urlpatterns = [
    url(r'^$', views.model_list, name='models'),
    url(r'^(?P<model_name>\w{0,20})/$', views.object_list, name='objectList'),  # accepting models with up to 20 chars
    url(r'^(?P<model_name>\w{0,20})/(?P<pk>[0-9]+)/$', views.object_detail, name='objectDetail'),
    url(r'^(?P<model_name>\w{0,20})/(?P<pk>[0-9]+)/delete/$', views.object_delete, name='objectDelete'),
    url(r'^(?P<model_name>\w{0,20})/(?P<pk>[0-9]+)/edit/$', views.object_update, name='objectEdit'),
    url(r'^(?P<model_name>\w{0,20})/create/$', views.object_create, name='modelCreate'),
]
