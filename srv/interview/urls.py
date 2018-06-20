from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('token', views.token, name='token'),
    path('code', views.code, name='code'),
]