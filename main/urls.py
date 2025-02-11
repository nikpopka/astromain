from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="main"),
    path('personal_account', views.personal_account, name="personal_account"),
    path('anketa', views.anketa, name="anketa"),
    path('administration_service', views.administration_service, name="administration_service"),
    path('administration_client', views.administration_client, name="administration_client"),
    path('administration_order', views.administration_order, name="administration_order"),
    path('edit_service/<int:id>', views.edit_service, name="edit_service"),
    path('edit_client/<int:id>', views.edit_client, name="edit_client"),
    path('delete_service/<int:id>', views.delete_service, name="delete_service"),
    path('delete_video/<int:id>', views.delete_video, name="delete_video"),
    path('delete_file/<int:id>', views.delete_file, name="delete_file"),

]