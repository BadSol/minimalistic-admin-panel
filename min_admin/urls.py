from django.conf.urls import url
import views

app_name = 'min_admin'
urlpatterns = [
    url(r'^$', views.index_view, name='models'),
    # url(r'^/(?P<model_name>\w+)/$', views.model_view, name='modelObjects'),
    url(r'^(?P<model_name>[\w]+)/$', views.model_view, name='modelObjects'),
]
