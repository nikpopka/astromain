from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('administration_service', views.administration_service, name="administration_service"),
    path('administration_client', views.administration_client, name="administration_client"),
    path('administration_order', views.administration_order, name="administration_order"),
    path('edit_service/<int:id>', views.edit_service, name="edit_service"),
    path('delete_service/<int:id>', views.delete_service, name="delete_service"),
]