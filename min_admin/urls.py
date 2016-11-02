from django.conf.urls import url
import views

app_name = 'min_admin'
urlpatterns = [
    url(r'^$', views.index_view, name='models'),
    url(r'^(?P<model_name>\w{0,20})/$', views.model_view, name='modelObjects'),  # accepting models with up to 20 chars
]
