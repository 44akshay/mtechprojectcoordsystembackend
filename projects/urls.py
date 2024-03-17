from django.urls import path
from . import views

urlpatterns = [

    # path('getProjects',views.get)
    path('postreq',views.send_project_reports,name='get_post_request'),
    path('projectDetails',views.project_details,name='project_details'),

    path('accept',views.accept_report,name='accept_report'),
    path('modify',views.modify_comment,name='modify_report'),
    path('',views.get_students,name='get_Students'),




]