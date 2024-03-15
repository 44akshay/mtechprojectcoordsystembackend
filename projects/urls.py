from django.urls import path
from . import views

urlpatterns = [

    
    path('',views.get_students,name='get_Students'),
    path('postreq',views.send_project_reports,name='get_post_request'),
    path('accept',views.accept_report,name='accept_report'),
    path('modify',views.modify_comment,name='modify_report'),



]