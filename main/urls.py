from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="main"),
    path('personal_account', views.personal_account, name="personal_account"),
    path('anketa', views.anketa, name="anketa"),
    path('services', views.services, name="services"),
    path('administration_service', views.administration_service, name="administration_service"),
    path('administration_client', views.administration_client, name="administration_client"),
    path('administration_about', views.administration_about, name="administration_about"),
    path('administration_anketa', views.administration_anketa, name="administration_anketa"),
    path('administration_links', views.administration_links, name="administration_links"),
    path('administration_promotions', views.administration_promotions, name="administration_promotions"),
    path('administration_comments', views.administration_comments, name="administration_comments"),
    path('delete_comment/<int:id>', views.delete_comment, name="delete_comment"),
    path('edit_service/<int:id>', views.edit_service, name="edit_service"),
    path('edit_client/<int:id>', views.edit_client, name="edit_client"),
    path('delete_service/<int:id>', views.delete_service, name="delete_service"),
    path('delete_video/<int:id>', views.delete_video, name="delete_video"),
    path('delete_file/<int:id>', views.delete_file, name="delete_file"),
    path('edit_question/<int:id>', views.edit_question, name="edit_question"),
    path('delete_question/<int:id>', views.delete_question, name="delete_question"),
    path('comments', views.comments, name="comments"),
    path('sent_message', views.sent_message, name="sent_message"),


]